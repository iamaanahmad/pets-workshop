import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the server directory to the path so we can import from models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app  # Changed from relative import to absolute import
from models.dog import Dog

# filepath: server/test_app.py
class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test client using Flask's test client
        self.app = app.test_client()
        self.app.testing = True
        # Turn off database initialization for tests
        app.config['TESTING'] = True
        
    def _create_mock_dog(self, dog_id, name, breed):
        """Helper method to create a mock dog with standard attributes"""
        dog = MagicMock(spec=['to_dict', 'id', 'name', 'breed'])
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        dog.to_dict.return_value = {'id': dog_id, 'name': name, 'breed': breed}
        return dog
        
    def _setup_query_mock(self, mock_query, dogs):
        """Helper method to configure the query mock"""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.all.return_value = dogs
        return mock_query_instance

    @patch('app.db.session.query')
    def test_get_dogs_success(self, mock_query):
        """Test successful retrieval of multiple dogs"""
        # Arrange
        dog1 = self._create_mock_dog(1, "Buddy", "Labrador")
        dog2 = self._create_mock_dog(2, "Max", "German Shepherd")
        mock_dogs = [dog1, dog2]
        
        self._setup_query_mock(mock_query, mock_dogs)
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        
        # Verify first dog
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['name'], "Buddy")
        self.assertEqual(data[0]['breed'], "Labrador")
        
        # Verify second dog
        self.assertEqual(data[1]['id'], 2)
        self.assertEqual(data[1]['name'], "Max")
        self.assertEqual(data[1]['breed'], "German Shepherd")
        
        # Verify query was called
        mock_query.assert_called_once()
        
    @patch('app.db.session.query')
    def test_get_dogs_empty(self, mock_query):
        """Test retrieval when no dogs are available"""
        # Arrange
        self._setup_query_mock(mock_query, [])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
        
    @patch('app.db.session.query')
    def test_get_dogs_structure(self, mock_query):
        """Test the response structure for a single dog"""
        # Arrange
        dog = self._create_mock_dog(1, "Buddy", "Labrador")
        self._setup_query_mock(mock_query, [dog])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(set(data[0].keys()), {'id', 'name', 'breed'})

    def test_dog_age_validation_valid_ages(self):
        """Test that valid ages (0-20) are accepted"""
        dog = Dog()
        
        # Test boundary values and some valid ages
        valid_ages = [0, 1, 5, 10, 15, 20]
        
        for age in valid_ages:
            with self.subTest(age=age):
                # This should not raise an exception
                validated_age = dog.validate_age('age', age)
                self.assertEqual(validated_age, age)
    
    def test_dog_age_validation_invalid_ages(self):
        """Test that invalid ages raise ValueError"""
        dog = Dog()
        
        # Test ages outside the valid range
        invalid_ages = [-1, -10, 21, 25, 50]
        
        for age in invalid_ages:
            with self.subTest(age=age):
                with self.assertRaises(ValueError) as context:
                    dog.validate_age('age', age)
                self.assertIn("Age must be between 0 and 20 years", str(context.exception))
    
    def test_dog_age_validation_none_value(self):
        """Test that None age raises ValueError"""
        dog = Dog()
        
        with self.assertRaises(ValueError) as context:
            dog.validate_age('age', None)
        self.assertIn("Age cannot be empty", str(context.exception))
    
    def test_dog_age_validation_non_integer(self):
        """Test that non-integer ages raise ValueError"""
        dog = Dog()
        
        invalid_types = ["5", 5.5, "ten", [], {}]
        
        for invalid_age in invalid_types:
            with self.subTest(age=invalid_age):
                with self.assertRaises(ValueError) as context:
                    dog.validate_age('age', invalid_age)
                self.assertIn("Age must be an integer", str(context.exception))


if __name__ == '__main__':
    unittest.main()