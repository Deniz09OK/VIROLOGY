"""
Server-side crack module — offline hash cracking.
T1110: Brute Force
"""
from __future__ import annotations
import hashlib


def crack_ntlm(ntlm_hash: str, wordlist_path: str) -> str | None:
    """Try to crack an NTLM hash against a wordlist. Returns plaintext or None."""
    with open(wordlist_path, "r", errors="ignore") as fh:
        for word in fh:
            word = word.strip()
            candidate = hashlib.new("md4", word.encode("utf-16-le")).hexdigest()
            if candidate.lower() == ntlm_hash.lower():
                return word
    return None
