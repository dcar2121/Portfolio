"""Sovereign signal: seed-backed identity/attribute for tokens."""
from dataclasses import dataclass
from typing import Optional
import hashlib


@dataclass
class SovereignSignal:
    """Simple wrapper for a sovereign seed/identity.

    Note: This module stores seeds in-memory only. Do NOT persist secrets
    to shared locations. Use HSM or secure keystores in production.
    """
    seed: str

    def id(self) -> str:
        """Derive a stable identifier from the seed (SHA256 hex)."""
        return hashlib.sha256(self.seed.encode("utf-8")).hexdigest()

    def verify_identity(self, claimant_seed: str) -> bool:
        """Verify a claimant by comparing derived identifiers.

        This is a placeholder for a cryptographic verification (e.g., sigs).
        """
        return self.id() == hashlib.sha256(claimant_seed.encode("utf-8")).hexdigest()


def example():
    s = SovereignSignal(seed="example-seed-1234")
    print("Sovereign ID:", s.id())


if __name__ == "__main__":
    example()
