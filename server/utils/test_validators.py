# filepath: server/utils/test_validators.py
import unittest
import sys
import os

# Add the server directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import validate_dog_age, validate_dog_age_safe


class TestDogAgeValidation(unittest.TestCase):
    """Test cases for dog age validation functions"""

    def test_validate_dog_age_valid_boundary_values(self):
        """Test that boundary values (0 and 20) are accepted"""
        self.assertEqual(validate_dog_age(0), 0)
        self.assertEqual(validate_dog_age(20), 20)

    def test_validate_dog_age_valid_middle_values(self):
        """Test that middle values are accepted"""
        valid_ages = [1, 5, 10, 15, 19]
        for age in valid_ages:
            with self.subTest(age=age):
                self.assertEqual(validate_dog_age(age), age)

    def test_validate_dog_age_invalid_negative_values(self):
        """Test that negative values raise ValueError"""
        invalid_ages = [-1, -5, -10, -100]
        for age in invalid_ages:
            with self.subTest(age=age):
                with self.assertRaises(ValueError) as context:
                    validate_dog_age(age)
                self.assertEqual(str(context.exception), "Age must be between 0 and 20 years")

    def test_validate_dog_age_invalid_high_values(self):
        """Test that values above 20 raise ValueError"""
        invalid_ages = [21, 25, 50, 100]
        for age in invalid_ages:
            with self.subTest(age=age):
                with self.assertRaises(ValueError) as context:
                    validate_dog_age(age)
                self.assertEqual(str(context.exception), "Age must be between 0 and 20 years")

    def test_validate_dog_age_none_value(self):
        """Test that None raises ValueError"""
        with self.assertRaises(ValueError) as context:
            validate_dog_age(None)
        self.assertEqual(str(context.exception), "Age cannot be empty")

    def test_validate_dog_age_non_integer_values(self):
        """Test that non-integer values raise ValueError"""
        invalid_types = [
            "5",         # string
            5.5,         # float
            "ten",       # text string
            [],          # list
            {},          # dict
            True,        # boolean
            set(),       # set
        ]
        
        for invalid_age in invalid_types:
            with self.subTest(age=invalid_age, type=type(invalid_age).__name__):
                with self.assertRaises(ValueError) as context:
                    validate_dog_age(invalid_age)
                self.assertEqual(str(context.exception), "Age must be an integer")

    def test_validate_dog_age_safe_valid_values(self):
        """Test that validate_dog_age_safe returns (True, age) for valid values"""
        valid_ages = [0, 1, 5, 10, 15, 20]
        for age in valid_ages:
            with self.subTest(age=age):
                is_valid, result = validate_dog_age_safe(age)
                self.assertTrue(is_valid)
                self.assertEqual(result, age)

    def test_validate_dog_age_safe_invalid_values(self):
        """Test that validate_dog_age_safe returns (False, error_message) for invalid values"""
        test_cases = [
            (-1, "Age must be between 0 and 20 years"),
            (21, "Age must be between 0 and 20 years"),
            (None, "Age cannot be empty"),
            ("5", "Age must be an integer"),
            (5.5, "Age must be an integer"),
        ]
        
        for age, expected_error in test_cases:
            with self.subTest(age=age):
                is_valid, result = validate_dog_age_safe(age)
                self.assertFalse(is_valid)
                self.assertEqual(result, expected_error)

    def test_validate_dog_age_with_realistic_dog_ages(self):
        """Test with realistic dog ages from the CSV data"""
        # Ages from the CSV file range from 1-15, all should be valid
        csv_ages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        for age in csv_ages:
            with self.subTest(age=age):
                self.assertEqual(validate_dog_age(age), age)
                is_valid, result = validate_dog_age_safe(age)
                self.assertTrue(is_valid)
                self.assertEqual(result, age)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
