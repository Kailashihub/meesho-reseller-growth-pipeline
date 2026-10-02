import csv
import tempfile
import unittest
from pathlib import Path
from growth_engine import ValidationError, load_feed, calculate_growth, run

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "monthly_category_revenue.csv"
CORRUPTED = HERE / "fixtures" / "corrupted_feed.csv"

class GrowthEngineTests(unittest.TestCase):
    def test_valid_fixture_loads(self):
        rows = load_feed(FIXTURE)
        self.assertEqual(len(rows), 15)
        self.assertEqual(set(rows[0]), {"month","category","revenue","n_orders"})

    def test_growth_marks_large_movement(self):
        rows = load_feed(FIXTURE)
        results = calculate_growth(rows, threshold=0.20)
        self.assertTrue(any(r["significant_change"] for r in results))
        self.assertTrue(all(r["mom_growth"] is None for r in results if r["month"] == "April"))

    def test_corrupted_feed_rejected(self):
        with self.assertRaises(ValidationError):
            load_feed(CORRUPTED)

    def test_output_is_written(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "growth.csv"
            run(FIXTURE, out)
            self.assertTrue(out.exists())
            with out.open(encoding="utf-8") as f:
                self.assertGreaterEqual(sum(1 for _ in csv.DictReader(f)), 15)

if __name__ == "__main__":
    unittest.main()
