# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from datetime import datetime
import time
from typing import Dict, Optional, Callable, Any

from azure.core.exceptions import ClientAuthenticationError

from .._constants import DEVELOPER_SIGN_ON_CLIENT_ID
from .._internal import InteractiveCredential, wrap_exceptions


class DeviceCodeCredential(InteractiveCredential):
    """Authenticates users through the device code flow.

    When :func:`get_token` is called, this credential acquires a verification URL and code from Azure Active Directory.
    A user must browse to the URL, enter the code, and authenticate with Azure Active Directory. If the user
    authenticates successfully, the credential receives an access token.

    This credential is primarily useful for authenticating a user in an environment without a web browser, such as an
    SSH session. If a web browser is available, :class:`~azure.identity.InteractiveBrowserCredential` is more
    convenient because it automatically opens a browser to the login page.

    :param str client_id: client ID of the application users will authenticate to. When not specified users will
        authenticate to an Azure development application.

    :keyword str authority: Authority of an Azure Active Directory endpoint, for example "login.microsoftonline.com",
        the authority for Azure Public Cloud (which is the default). :class:`~azure.identity.AzureAuthorityHosts`
        defines authorities for other clouds.
    :keyword str tenant_id: an Azure Active Directory tenant ID. Defaults to the "organizations" tenant, which can
        authenticate work or school accounts. **Required for single-tenant applications.**
    :keyword int timeout: seconds to wait for the user to authenticate. Defaults to the validity period of the
        device code as set by Azure Active Directory, which also prevails when **timeout** is longer.
    :keyword prompt_callback: A callback enabling control of how authentication
        instructions are presented. Must accept arguments (``verification_uri``, ``user_code``, ``expires_on``):

        - ``verification_uri`` (str) the URL the user must visit
        - ``user_code`` (str) the code the user must enter there
        - ``expires_on`` (datetime.datetime) the UTC time at which the code will expire
        If this argument isn't provided, the credential will print instructions to stdout.
    :paramtype prompt_callback: Callable[str, str, ~datetime.datetime]
    :keyword AuthenticationRecord authentication_record: :class:`AuthenticationRecord` returned by :func:`authenticate`
    :keyword bool disable_automatic_authentication: if True, :func:`get_token` will raise
        :class:`AuthenticationRequiredError` when user interaction is required to acquire a token. Defaults to False.
    :keyword cache_persistence_options: configuration for persistent token caching. If unspecified, the credential
        will cache tokens in memory.
    :paramtype cache_persistence_options: ~azure.identity.TokenCachePersistenceOptions
    :keyword bool disable_authority_validation_and_instance_discovery: Determines whether or not instance discovery
        is performed when attempting to authenticate. Setting this to true will completely disable instance discovery
        and authority validation.

    .. admonition:: Example:

        .. literalinclude:: ../samples/credential_creation_code_snippets.py
            :start-after: [START create_device_code_credential]
            :end-before: [END create_device_code_credential]
            :language: python
            :dedent: 4
            :caption: Create a DeviceCodeCredential.
    """

    def __init__(
            self,
            client_id: str = DEVELOPER_SIGN_ON_CLIENT_ID,
            *,
            timeout: Optional[int] = None,
            prompt_callback: Optional[Callable[[str, str, datetime], None]] = None,
            **kwargs: Any
    ) -> None:
        self._timeout = timeout
        self._prompt_callback = prompt_callback
        super(DeviceCodeCredential, self).__init__(client_id=client_id, **kwargs)

    @wrap_exceptions
    def _request_token(self, *scopes: str, **kwargs: Any) -> Dict:
        # MSAL requires scopes be a list
        scopes = list(scopes)  # type: ignore

        app = self._get_app(**kwargs)
        flow = app.initiate_device_flow(scopes)
        if "error" in flow:
            raise ClientAuthenticationError(
                message="Couldn't begin authentication: {}".format(flow.get("error_description") or flow.get("error"))
            )

        if self._prompt_callback:
            self._prompt_callback(
                flow["verification_uri"], flow["user_code"], datetime.utcfromtimestamp(flow["expires_at"])
            )
        else:
            print(flow["message"])

        if self._timeout is not None and self._timeout < flow["expires_in"]:
            # user specified an effective timeout we will observe
            deadline = int(time.time()) + self._timeout
            result = app.acquire_token_by_device_flow(
                flow, exit_condition=lambda flow: time.time() > deadline, claims_challenge=kwargs.get("claims")
            )
        else:
            # MSAL will stop polling when the device code expires
            result = app.acquire_token_by_device_flow(flow, claims_challenge=kwargs.get("claims"))

        # raise for a timeout here because the error is particular to this class
        if "access_token" not in result and result.get("error") == "authorization_pending":
            raise ClientAuthenticationError(message="Timed out waiting for user to authenticate")

        # base class will raise for other errors
        return result
