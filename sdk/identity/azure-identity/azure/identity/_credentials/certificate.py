# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from binascii import hexlify
from typing import cast, NamedTuple, Union, Dict, Any, Optional

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.backends import default_backend
import six

from .._internal import validate_tenant_id
from .._internal.client_credential_base import ClientCredentialBase


class CertificateCredential(ClientCredentialBase):
    """Authenticates as a service principal using a certificate.

    The certificate must have an RSA private key, because this credential signs assertions using RS256. See
    `Azure Active Directory documentation
    <https://docs.microsoft.com/azure/active-directory/develop/active-directory-certificate-credentials#register-your-certificate-with-microsoft-identity-platform>`_
    for more information on configuring certificate authentication.

    :param str tenant_id: ID of the service principal's tenant. Also called its "directory" ID.
    :param str client_id: The service principal's client ID
    :param str certificate_path: Optional path to a certificate file in PEM or PKCS12 format, including the private
        key. If not provided, **certificate_data** is required.

    :keyword str authority: Authority of an Azure Active Directory endpoint, for example "login.microsoftonline.com",
        the authority for Azure Public Cloud (which is the default). :class:`~azure.identity.AzureAuthorityHosts`
        defines authorities for other clouds.
    :keyword bytes certificate_data: The bytes of a certificate in PEM or PKCS12 format, including the private key
    :keyword password: The certificate's password. If a unicode string, it will be encoded as UTF-8. If the certificate
        requires a different encoding, pass appropriately encoded bytes instead.
    :paramtype password: str or bytes
    :keyword bool send_certificate_chain: If True, the credential will send the public certificate chain in the x5c
        header of each token request's JWT. This is required for Subject Name/Issuer (SNI) authentication. Defaults to
        False.
    :keyword cache_persistence_options: Configuration for persistent token caching. If unspecified, the credential
        will cache tokens in memory.
    :paramtype cache_persistence_options: ~azure.identity.TokenCachePersistenceOptions
    :keyword bool disable_authority_validation_and_instance_discovery: Determines whether or not instance discovery
        is performed when attempting to authenticate. Setting this to true will completely disable instance discovery
        and authority validation.
    :keyword List[str] additionally_allowed_tenants: Specifies tenants in addition to the specified "tenant_id"
        for which the credential may acquire tokens. Add the wildcard value "*" to allow the credential to
        acquire tokens for any tenant the application can access.

    .. admonition:: Example:

        .. literalinclude:: ../samples/credential_creation_code_snippets.py
            :start-after: [START create_certificate_credential]
            :end-before: [END create_certificate_credential]
            :language: python
            :dedent: 4
            :caption: Create a CertificateCredential.
    """

    def __init__(
            self,
            tenant_id: str,
            client_id: str,
            certificate_path: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        validate_tenant_id(tenant_id)

        client_credential = get_client_credential(certificate_path, **kwargs)

        super(CertificateCredential, self).__init__(
            client_id=client_id,
            client_credential=client_credential,
            tenant_id=tenant_id,
            **kwargs
        )


def extract_cert_chain(pem_bytes: bytes) -> bytes:
    """Extract a certificate chain from a PEM file's bytes, removing line breaks."""

    # if index raises ValueError, there's no PEM-encoded cert
    start = pem_bytes.index(b"-----BEGIN CERTIFICATE-----")
    footer = b"-----END CERTIFICATE-----"
    end = pem_bytes.rindex(footer)
    chain = pem_bytes[start : end + len(footer) + 1]

    return b"".join(chain.splitlines())


_Cert = NamedTuple("_Cert", [("pem_bytes", bytes), ("private_key", "Any"), ("fingerprint", bytes)])


def load_pem_certificate(
        certificate_data: bytes,
        password: Optional[bytes] = None
) -> _Cert:
    private_key = serialization.load_pem_private_key(certificate_data, password, backend=default_backend())
    cert = x509.load_pem_x509_certificate(certificate_data, default_backend())
    fingerprint = cert.fingerprint(hashes.SHA1())  # nosec
    return _Cert(certificate_data, private_key, fingerprint)


def load_pkcs12_certificate(
        certificate_data: bytes,
        password: Optional[bytes] = None
) -> _Cert:
    from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, pkcs12, PrivateFormat

    try:
        private_key, cert, additional_certs = pkcs12.load_key_and_certificates(
            certificate_data, password, backend=default_backend()
        )
    except ValueError as ex:
        # mentioning PEM here because we raise this error when certificate_data is garbage
        six.raise_from(ValueError("Failed to deserialize certificate in PEM or PKCS12 format"), ex)
    if not private_key:
        raise ValueError("The certificate must include its private key")
    if not cert:
        raise ValueError("Failed to deserialize certificate in PEM or PKCS12 format")

    # This serializes the private key without any encryption it may have had. Doing so doesn't violate security
    # boundaries because this representation of the key is kept in memory. We already have the key and its
    # password, if any, in memory.
    key_bytes = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    pem_sections = [key_bytes] + [c.public_bytes(Encoding.PEM) for c in [cert] + additional_certs]
    pem_bytes = b"".join(pem_sections)

    fingerprint = cert.fingerprint(hashes.SHA1())  # nosec

    return _Cert(pem_bytes, private_key, fingerprint)


def get_client_credential(
        certificate_path: Optional[str] = None,
        password: Optional[Union[bytes, str]] = None,
        certificate_data: Optional[bytes] = None,
        send_certificate_chain: bool = False,
        **_: Any
) -> Dict:
    """Load a certificate from a filesystem path or bytes, return it as a dict suitable for msal.ClientApplication"""

    if certificate_path:
        if certificate_data:
            raise ValueError('Please specify either "certificate_path" or "certificate_data", not both')
        with open(certificate_path, "rb") as f:
            certificate_data = f.read()
    elif not certificate_data:
        raise ValueError('CertificateCredential requires a value for either "certificate_path" or "certificate_data"')

    if password:
        # if password is already bytes, this won't change its encoding
        password = six.ensure_binary(password, "utf-8")
    password = cast("Optional[bytes]", password)

    if b"-----BEGIN" in certificate_data:
        cert = load_pem_certificate(certificate_data, password)
    else:
        cert = load_pkcs12_certificate(certificate_data, password)
        password = None  # load_pkcs12_certificate returns cert.pem_bytes decrypted

    if not isinstance(cert.private_key, RSAPrivateKey):
        raise ValueError("The certificate must have an RSA private key because RS256 is used for signing")

    client_credential = {"private_key": cert.pem_bytes, "thumbprint": hexlify(cert.fingerprint).decode("utf-8")}
    if password:
        client_credential["passphrase"] = password

    if send_certificate_chain:
        try:
            # the JWT needs the whole chain but load_pem_x509_certificate deserializes only the signing cert
            chain = extract_cert_chain(cert.pem_bytes)
            client_credential["public_certificate"] = six.ensure_str(chain)
        except ValueError as ex:
            # we shouldn't land here--cryptography already loaded the cert and would have raised if it were malformed
            six.raise_from(ValueError("Malformed certificate"), ex)

    return client_credential
