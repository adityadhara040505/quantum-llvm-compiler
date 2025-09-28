"""
Noise-aware scheduler: a small heuristic to prefer lower-error qubits for single-qubit gates,
and to choose connected pairs for 2-qubit gates based on topology.
"""

class NoiseAwareScheduler:
    def __init__(self, hardware_profile=None):
        # hardware_profile: dict with keys:
        # - error_rates: {qubit_index: error_rate}
        # - topology: list of (i,j) edges
        self.hw = hardware_profile or {}
        self.error_rates = self.hw.get('error_rates', {})
        self.topology = set(tuple(sorted(e)) for e in self.hw.get('topology', []))

    def pick_qubit_for_single(self, candidates):
        # pick the candidate with smallest error rate
        best = min(candidates, key=lambda q: self.error_rates.get(q, 1.0))
        return best

    def pick_pair_for_two_qubit(self, candidate_pairs):
        # choose a pair that exists in topology and minimizes total error
        ranked = []
        for (a, b) in candidate_pairs:
            edge = tuple(sorted((a, b)))
            if edge in self.topology:
                score = self.error_rates.get(a, 0.01) + self.error_rates.get(b, 0.01)
                ranked.append(((a, b), score))
        if not ranked:
            # fallback: choose pair with lowest combined error
            return min(candidate_pairs, key=lambda p: self.error_rates.get(p[0], 1.0) + self.error_rates.get(p[1], 1.0))
        ranked.sort(key=lambda x: x[1])
        return ranked[0][0]
