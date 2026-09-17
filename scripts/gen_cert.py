"""
Generates a self-signed RSA-2048 TLS certificate masquerading as update.microsoft.com.
Outputs certs/cert.pem and certs/key.pem.
"""
from __future__ import annotations

import datetime
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

CERTS_DIR = Path(__file__).parent.parent / "certs"
CERT_FILE = CERTS_DIR / "cert.pem"
KEY_FILE  = CERTS_DIR / "key.pem"

CN = "update.microsoft.com"
SAN = [
    x509.DNSName("update.microsoft.com"),
    x509.DNSName("*.update.microsoft.com"),
]


def generate() -> None:
    CERTS_DIR.mkdir(exist_ok=True)

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    KEY_FILE.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Washington"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Microsoft Corporation"),
        x509.NameAttribute(NameOID.COMMON_NAME, CN),
    ])

    now = datetime.datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=3650))
        .add_extension(x509.SubjectAlternativeName(SAN), critical=False)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )

    CERT_FILE.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    print(f"[+] cert -> {CERT_FILE}")
    print(f"[+] key  -> {KEY_FILE}")


if __name__ == "__main__":
    generate()
