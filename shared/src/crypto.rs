// AES-256-GCM (session payloads) + RSA-4096 (key exchange) — T1573.002

pub struct SessionKey(Vec<u8>);

pub struct KeyPair {
    pub private_pem: String,
    pub public_pem: String,
}

impl SessionKey {
    pub fn from_bytes(bytes: Vec<u8>) -> Self {
        Self(bytes)
    }

    pub fn as_bytes(&self) -> &[u8] {
        &self.0
    }
}

// Nonce (12 bytes) is prepended to the ciphertext in the output buffer.
pub fn encrypt(_key: &SessionKey, _plaintext: &[u8]) -> Result<Vec<u8>, String> {
    todo!("AES-256-GCM encrypt with OsRng nonce prepended")
}

pub fn decrypt(_key: &SessionKey, _data: &[u8]) -> Result<Vec<u8>, String> {
    todo!("split nonce [0..12] | ciphertext [12..] then AES-256-GCM decrypt")
}

pub fn generate_session_key() -> SessionKey {
    todo!("32-byte OsRng key → SessionKey")
}

pub fn generate_rsa_keypair() -> Result<KeyPair, String> {
    todo!("RSA-4096 keygen via rsa crate, PEM-encode both halves")
}

pub fn rsa_encrypt_session_key(_public_pem: &str, _key: &SessionKey) -> Result<Vec<u8>, String> {
    todo!("RSA-OAEP-SHA256 encrypt session key bytes with recipient public key")
}

pub fn rsa_decrypt_session_key(_private_pem: &str, _blob: &[u8]) -> Result<SessionKey, String> {
    todo!("RSA-OAEP-SHA256 decrypt → SessionKey")
}
