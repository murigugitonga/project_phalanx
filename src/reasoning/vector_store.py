"""
This engine uses basic math vectors (or can integrate with lightweight tools) to track, 
score & rank incoming target frames against a localized list of Rules of Engagement (ROE) rules.
"""

import math
from typing import List, Dict, Any

class PureTacticalVectorStore:
    def __init__(self):
        # Local air-gapped storage for rules of engagement parameters
        self.kb_store: List[Dict[str, Any]] = []
        print("[INIT] Pure-Python Local Semantic Knowledge Store activated.")

    def seed_rules_of_engagement(self):
        """Mocks air-gapped semantic embeddings of military rules of engagement"""
        self.kb_store = [
            {
                "rule_id": "ROE-01-AIR",
                "condition": "Unidentified airborne asset exceeding Mach 1 inside restricted military corridor",
                "vector": [0.9, 0.1, 0.8, 0.4], # Normalized target semantic vector
                "action": "TRIGGER_INTERCEPT_SCRAMBLE"
            },
            {
                "rule_id": "ROE-02-MARITIME",
                "condition": "Subsurface vessel displaying non-allied transponder metrics inside maritime borders",
                "vector": [0.1, 0.9, 0.2, 0.7],
                "action": "EMIT_SONAR_CHALLENGE"
            },
            {
                "rule_id": "ROE-03-CIVILIAN",
                "condition": "Commercial or low-velocity domestic aircraft on declared flight plan trajectory",
                "vector": [0.2, 0.1, 0.1, 0.1],
                "action": "MONITOR_PASSIVE"
            }
        ]
        print(f"[SEED SUCCESS] {len(self.kb_store)} operational rule metrics written to tactical memory.")

    @staticmethod
    def calculate_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Computes the semantic proximity match score between two vectors"""
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def evaluate_threat_vector(self, query_vector: List[float]) -> Dict[str, Any]:
        """Queries the vector index to find the highest match rule"""
        best_match = None
        highest_score = -1.0

        for rule in self.kb_store:
            similarity = self.calculate_cosine_similarity(query_vector, rule["vector"])
            if similarity > highest_score:
                highest_score = similarity
                best_match = rule

        return {
            "matched_rule_id": best_match["rule_id"] if best_match else "UNKNOWN",
            "action_directive": best_match["action"] if best_match else "HOLD_FIRE",
            "confidence_score": round(highest_score, 4)
        }

# Single-pass execution validation check
if __name__ == "__main__":
    store = PureTacticalVectorStore()
    store.seed_rules_of_engagement()
    # Mocking a high-speed airborne target vector profile
    incoming_radar_vector = [0.85, 0.12, 0.78, 0.35]
    result = store.evaluate_threat_vector(incoming_radar_vector)
    print(f"[INDEX TEST RESULT] Highest Match: {result['matched_rule_id']} | Action: {result['action_directive']} (Score: {result['confidence_score']})")
