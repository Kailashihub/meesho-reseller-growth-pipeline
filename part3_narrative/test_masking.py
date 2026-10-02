import unittest
from masking import mask_unverified_numbers

class MaskingTests(unittest.TestCase):
    def test_unverified_number_is_masked(self):
        self.assertEqual(mask_unverified_numbers("Claim 9999"), "Claim [MASKED]")

    def test_allowed_number_is_preserved(self):
        self.assertEqual(mask_unverified_numbers("Revenue 1000", {"1000"}), "Revenue 1000")

if __name__ == "__main__":
    unittest.main()
