// All C2 connection parameters — strings obfuscated at compile time via obfstr — T1027

pub const C2_HOST: &str = "192.168.56.112";
pub const C2_PORT: u16 = 443;
pub const BEACON_INTERVAL_MS: u64 = 5_000;
pub const BEACON_JITTER_MS: u64 = 2_000;
// SHA-256 fingerprint of the C2 TLS certificate (pinned — T1573.002)
pub const CERT_FINGERPRINT: &str = "";
