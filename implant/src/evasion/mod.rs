// AV/EDR evasion — API hashing, string obfuscation, direct syscalls — T1562.001, TA0005
//
// api_hashing  : resolve WinAPI exports at runtime via hash comparison (hides IAT entries)
// obfuscation  : compile-time string obfuscation via obfstr (no plain-text IOCs in binary)
