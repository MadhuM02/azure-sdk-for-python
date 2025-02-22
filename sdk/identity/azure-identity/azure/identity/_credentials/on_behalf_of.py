# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import time
from typing import Any, Optional

import six
import msal

from azure.core.credentials import AccessToken
from azure.core.exceptions import ClientAuthenticationError

from .certificate import get_client_credential
from .._internal.decorators import wrap_exceptions
from .._internal.get_token_mixin import GetTokenMixin
from .._internal.interactive import _build_auth_record
from .._internal.msal_credentials import MsalCredential
from .. import AuthenticationRecord

class OnBehalfOfCredential(MsalCredential, GetTokenMixin):
    """Authenticates a service principal via the on-behalf-of flow.

    This flow is typically used by middle-tier services that authorize requests to other services with a delegated
    user identity. Because this is not an interactive authentication flow, an application using it must have admin
    consent for any delegated permissions before requesting tokens for them. See `Azure Active Directory documentation
    <https://docs.microsoft.com/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow>`_ for a more detailed
    description of the on-behalf-of flow.

    :param str tenant_id: ID of the service principal's tenant. Also called its "directory" ID.
    :param str client_id: The service principal's client ID
    :keyword str client_secret: Optional. A client secret to authenticate the service principal.
        Either **client_secret** or **client_certificate** must be provided.
    :keyword bytes client_certificate: Optional. The bytes of a certificate in PEM or PKCS12 format including
        the private key to authenticate the service principal. Either **client_secret** or **client_certificate** must
        be provided.
    :keyword str user_assertion: Required. The access token the credential will use as the user assertion when
        requesting on-behalf-of tokens

    :keyword str authority: Authority of an Azure Active Directory endpoint, for example "login.microsoftonline.com",
        the authority for Azure Public Cloud (which is the default). :class:`~azure.identity.AzureAuthorityHosts`
        defines authorities for other clouds.
    :keyword password: A certificate password. Used only when **client_certificate** is provided. If this value
        is a unicode string, it will be encoded as UTF-8. If the certificate requires a different encoding, pass
        appropriately encoded bytes instead.
    :paramtype password: str or bytes
    :keyword bool disable_authority_validation_and_instance_discovery: Determines whether or not instance discovery
        is performed when attempting to authenticate. Setting this to true will completely disable instance discovery
        and authority validation.
    :keyword List[str] additionally_allowed_tenants: Specifies tenants in addition to the specified "tenant_id"
        for which the credential may acquire tokens. Add the wildcard value "*" to allow the credential to
        acquire tokens for any tenant the application can access.

    .. admonition:: Example:

        .. literalinclude:: ../samples/credential_creation_code_snippets.py
            :start-after: [START create_on_behalf_of_credential]
            :end-before: [END create_on_behalf_of_credential]
            :language: python
            :dedent: 4
            :caption: Create an OnBehalfOfCredential.
    """

    def __init__(
            self,
            tenant_id: str,
            client_id: str,
            **kwargs: Any
    ) -> None:
        self._assertion = kwargs.pop("user_assertion", None)
        if not self._assertion:
            raise TypeError('"user_assertion" is required.')
        client_certificate = kwargs.pop("client_certificate", None)
        client_secret = kwargs.pop("client_secret", None)

        if client_certificate:
            if client_secret:
                raise ValueError('Specifying both "client_certificate" and "client_secret" is not valid.')
            try:
                credential = get_client_credential(
                    certificate_path=None, password=kwargs.pop("password", None), certificate_data=client_certificate
                )
            except ValueError as ex:
                # client_certificate isn't a valid cert.
                message = (
                    '"client_certificate" is not a valid certificate in PEM or PKCS12 format'
                )
                six.raise_from(ValueError(message), ex)
        elif client_secret:
            credential = client_secret
        else:
            raise TypeError('Either "client_certificate" or "client_secret" must be provided')

        super(OnBehalfOfCredential, self).__init__(
            client_id=client_id,
            client_credential=credential,
            tenant_id=tenant_id,
            **kwargs)
        self._auth_record: Optional[AuthenticationRecord] = None

    @wrap_exceptions
    def _acquire_token_silently(
        self, *scopes: str, **kwargs: Any
    ) -> Optional[AccessToken]:
        if self._auth_record:
            claims = kwargs.get("claims")
            app = self._get_app(**kwargs)
            for account in app.get_accounts(username=self._auth_record.username):
                if account.get("home_account_id") != self._auth_record.home_account_id:
                    continue

                now = int(time.time())
                result = app.acquire_token_silent_with_error(list(scopes), account=account, claims_challenge=claims)
                if result and "access_token" in result and "expires_in" in result:
                    return AccessToken(result["access_token"], now + int(result["expires_in"]))

        return None

    @wrap_exceptions
    def _request_token(self, *scopes: str, **kwargs: Any) -> AccessToken:
        app: msal.ConfidentialClientApplication = self._get_app(**kwargs)
        request_time = int(time.time())
        result = app.acquire_token_on_behalf_of(self._assertion, list(scopes), claims_challenge=kwargs.get("claims"))
        if "access_token" not in result or "expires_in" not in result:
            message = "Authentication failed: {}".format(result.get("error_description") or result.get("error"))
            response = self._client.get_error_response(result)
            raise ClientAuthenticationError(message=message, response=response)

        try:
            self._auth_record = _build_auth_record(result)
        except ClientAuthenticationError:
            pass  # non-fatal; we'll use the assertion again next time instead of a refresh token

        return AccessToken(result["access_token"], request_time + int(result["expires_in"]))
