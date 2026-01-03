"""Voting system that composes SovereignSignal, DataCoherenceSignal, and TransmissionSignalUtility."""
from typing import Dict, Any
from .sovereign_signal import SovereignSignal
from .data_coherence import data_coherence_signal
from .transmission_signal import TransmissionSignalUtility


class VotingSystem:
    def __init__(self, sovereign_seed: str):
        self.sovereign = SovereignSignal(sovereign_seed)
        self.coherence_history = []
        self.transmission = TransmissionSignalUtility()
        self.vote_count: Dict[str, int] = {}

    def observe_network(self, metric_value: float):
        """Record a new network metric (e.g., proportion of responsive nodes)."""
        self.coherence_history.append(metric_value)

    def current_coherence(self):
        return data_coherence_signal(self.coherence_history)

    def cast_vote(self, claimant_seed: str, voter_id: str) -> Dict[str, Any]:
        """Attempt to cast a vote from claimant with seed and voter_id.

        Returns a dict describing the result and costs.
        """
        # Verify sovereign identity (placeholder)
        if not self.sovereign.verify_identity(claimant_seed):
            return {"ok": False, "reason": "identity_verification_failed"}

        # Coherence check: simple threshold on last coherence value
        coherence = self.current_coherence()
        if coherence and coherence[-1] < 0.5:
            return {"ok": False, "reason": "low_coherence", "coherence": coherence[-1]}

        # Transmission cost and spam prevention
        cost = self.transmission.transmit()
        if self.vote_count.get(voter_id, 0) >= 1:
            return {"ok": False, "reason": "excessive_voting", "cost": cost}

        # Accept the vote
        self.vote_count[voter_id] = self.vote_count.get(voter_id, 0) + 1
        return {"ok": True, "tx_cost": cost}


def example():
    vs = VotingSystem("example-seed-1234")
    # seed some coherence observations
    for v in [0.9, 0.95, 0.92]:
        vs.observe_network(v)
    print(vs.cast_vote("example-seed-1234", "voter-1"))
    print(vs.cast_vote("bad-seed", "voter-2"))


if __name__ == "__main__":
    example()
