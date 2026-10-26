"""Validate the exercise inventory; this does not measure model activation."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class EvalInventoryTests(unittest.TestCase):
    def test_each_skill_has_positive_and_near_miss_cases(self):
        names = {path.name for path in (ROOT / "skills").iterdir()}
        cases = json.loads((ROOT / "evals/activation-cases.json").read_text())
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        for case in cases:
            self.assertTrue(case["checks"], case["id"])
            self.assertTrue(set(case["expected"]) <= names)
            self.assertTrue(set(case["excluded"]) <= names)
            self.assertFalse(set(case["expected"]) & set(case["excluded"]))
        for name in names:
            self.assertTrue(any(name in case["expected"] for case in cases), name)
            self.assertTrue(any(name in case["excluded"] for case in cases), name)

    def test_x_routing_distinguishes_client_variant_from_model(self):
        cases = {case["id"]: case for case in json.loads(
            (ROOT / "evals/activation-cases.json").read_text())}
        self.assertEqual(cases["grok-native-x"]["expected"], [])
        self.assertEqual(cases["grok-explicit-mamitsu-x"]["expected"], ["mamitsu"])
        self.assertIn("x-post-extraction", cases["grok-model-in-pi"]["expected"])
        self.assertEqual(cases["grok-x-integration"]["expected"], ["mamitsu-app-integration"])


if __name__ == "__main__":
    unittest.main()
