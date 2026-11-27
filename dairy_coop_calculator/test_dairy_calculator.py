"""Tests for the dairy co-op payment calculator.

Commentary: these tests cover normal calculations, the three farmer examples,
the invalid text case, and invalid non-positive values.
"""

import unittest

from dairy_calculator import calculate_payment, get_current_price


class DairyCalculatorTests(unittest.TestCase):
    def test_default_weekly_price(self):
        self.assertEqual(get_current_price(), 55.0)

    def test_three_farmer_payments(self):
        examples = [(18.5, 55.0), (32.0, 55.0), (7.25, 55.0)]
        expected = [1017.5, 1760.0, 398.75]

        for (litres, price), expected_total in zip(examples, expected):
            with self.subTest(litres=litres):
                self.assertAlmostEqual(calculate_payment(litres, price), expected_total)

    def test_letters_are_not_accepted_as_litres(self):
        with self.assertRaises(ValueError):
            calculate_payment(float("letters"), 55.0)

    def test_zero_and_negative_litres_are_rejected(self):
        for litres in (0, -1):
            with self.subTest(litres=litres):
                with self.assertRaises(ValueError):
                    calculate_payment(litres, 55.0)


if __name__ == "__main__":
    unittest.main()
