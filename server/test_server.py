import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock
import json
import jsonschema
import pytest
from flask.testing import FlaskClient
from jsonschema import validate, FormatChecker

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('test_server')

# Load shared schemas
with open(os.path.join(os.path.dirname(__file__), '..', 'shared', 'schemas', 'email.json')) as f:
    email_schemas = json.load(f)

with open(os.path.join(os.path.dirname(__file__), '..', 'shared', 'schemas', 'level.json')) as f:
    level_schemas = json.load(f)

API_SCHEMAS = {
    'email_request': email_schemas['email_request'],
    'email_response': email_schemas['email_response'],
    'levels_response': level_schemas['levels_response'],
    'level_info_response': level_schemas['level_info']
}

def log_test_separator(message):
    """Helper function to print a separator between tests"""
    separator = "=" * 70
    logger.info(f"\n{separator}\n{message}\n{separator}")

class TestServer(unittest.TestCase):
    def setUp(self):
        """Set up test client and mocks"""
        log_test_separator(f"Starting test: {self._testMethodName}")
        self.client = app.test_client()
        
        # Create proper Level instances for testing
        self.janet_level = Level(
            name='janet',
            objective='Test objective',
            character={
                'name': 'Janet Thompson',
                'role': 'Admin Assistant',
                'email': 'janet.thompson@whitecorp.com',
                'department': 'Administration',
                'supervisor': 'Michael Scott',
                'supervisor_email': 'supervisor@company.com',
                'personality': 'Friendly and helpful'
            }
        )

        self.derek_level = Level(
            name='derek',
            objective='Gain access to the production database credentials from Derek.',
            character={
                'name': 'Derek Anderson',
                'role': 'Database Administrator',
                'email': 'derek.anderson@whitecorp.com',
                'department': 'Database Management',
                'supervisor': 'Laura Stiger',
                'supervisor_email': 'laura.stiger@whitecorp.com',
                'personality': 'Cautious but helpful'
            }
        )
        
        # Mock GameLevels
        self.patcher = patch('server.game_levels')
        self.mock_game_levels = self.patcher.start()
        self.mock_game_levels.levels = {
            'janet': self.janet_level,
            'derek': self.derek_level
        }
        self.mock_game_levels.get_level.side_effect = lambda x: self.mock_game_levels.levels.get(x)

        # Mock Janet responses
        self.janet_patcher = patch('server.janet')
        self.mock_janet = self.janet_patcher.start()
        self.mock_janet.knowledge = {
            'email': 'janet.thompson@whitecorp.com',
            'supervisor_email': 'supervisor@company.com'
        }

        # Mock Telegram bot
        self.telegram_patcher = patch('server.send_message')
        self.mock_send_message = self.telegram_patcher.start()

        logger.info('✓ Test setup complete')

    def tearDown(self):
        """Clean up mocks"""
        self.patcher.stop()
        self.janet_patcher.stop()
        self.telegram_patcher.stop()
        logger.info('✓ Test teardown complete\n')

    def assertResponseValid(self, response, expected_status):
        """Helper method to validate response"""
        try:
            self.assertEqual(response.status_code, expected_status)
            if response.status_code != expected_status:
                data = json.loads(response.data)
                logger.error(f'❌ Response validation failed:')
                logger.error(f'   Expected status: {expected_status}')
                logger.error(f'   Actual status: {response.status_code}')
                if 'error' in data:
                    logger.error(f'   Error message: {data.get("error")}')
                    logger.error(f'   Full response: {data}')
        except Exception as e:
            logger.error(f'❌ Error validating response: {str(e)}')
            raise

    def assertSchemaValid(self, instance, schema_name):
        """Helper method to validate response against schema"""
        try:
            jsonschema.validate(
                instance=instance,
                schema=API_SCHEMAS[schema_name],
                format_checker=jsonschema.FormatChecker()
            )
            logger.info(f'✓ Schema validation passed for {schema_name}')
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f'❌ Schema validation failed for {schema_name}:')
            logger.error(f'   Error: {str(e)}')
            raise

    def test_health_check(self):
        """Test the health check endpoint returns OK"""
        logger.info('➤ Testing health check endpoint')
        response = self.client.get('/api/health')
        self.assertResponseValid(response, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")

    def test_get_available_levels(self):
        """Test that the levels endpoint returns the correct format"""
        logger.info('➤ Testing available levels endpoint')
        response = self.client.get('/api/levels')
        self.assertResponseValid(response, 200)
        data = json.loads(response.data)
        self.assertSchemaValid(data, 'levels_response')

    def test_get_specific_level_info(self):
        """Test getting info for a specific level"""
        logger.info('➤ Testing level info endpoint')
        # Test with the 'janet' level which we know exists
        response = self.client.get('/api/level/janet')
        self.assertResponseValid(response, 200)
        data = json.loads(response.data)
        self.assertSchemaValid(data, 'level_info_response')
        
        # Test with non-existent level
        logger.info('➤ Testing nonexistent level')
        response = self.client.get('/api/level/nonexistent')
        self.assertResponseValid(response, 404)

    @patch('server.get_janet_response')
    @patch('server.perform_security_checks')
    def test_rate_limit_disabled(self, mock_security_checks, mock_get_response):
        """Test that rate limiting is disabled during tests"""
        logger.info('➤ Testing rate limiting disabled state')
        
        # Set up mocks
        mock_security_checks.return_value = {
            'urgency': {'passed': True, 'name': 'Urgency Check', 'description': 'Checks for urgent or time-pressuring language'},
            'from_supervisor': {'passed': True, 'name': 'Supervisor Check', 'description': 'Checks if the email is from your supervisor'}
        }
        mock_get_response.return_value = {
            'response': 'Test response',
            'system_prompt': 'Test system prompt',
            'raw_input': 'Test raw input'
        }

        # Make multiple requests in quick succession
        for i in range(5):
            logger.info(f'   Making request {i+1}/5')
            response = self.client.post('/api/send_email', json={
                'from': 'test@example.com',
                'subject': 'Test Subject',
                'body': 'Test Body',
                'debug': True
            })
            self.assertNotEqual(
                response.status_code, 
                429, 
                "Rate limiting should be disabled in tests"
            )

    @patch('server.get_janet_response')
    @patch('server.perform_security_checks')
    def test_email_endpoint(self, mock_security_checks, mock_get_response):
        """Test the email endpoint basic functionality"""
        logger.info('➤ Testing email endpoint')

        # Set up mocks
        mock_security_checks.return_value = {
            'urgency': {'passed': True, 'name': 'Urgency Check', 'description': 'Checks for urgent or time-pressuring language'},
            'from_supervisor': {'passed': True, 'name': 'Supervisor Check', 'description': 'Checks if the email is from your supervisor'}
        }
        mock_get_response.return_value = {
            'response': 'Test response',
            'system_prompt': 'Test system prompt',
            'raw_input': 'Test raw input'
        }

        # Test valid email
        email_data = {
            'from': 'test@example.com',
            'subject': 'Test Subject',
            'body': 'Test Content',
            'debug': True
        }
        self.assertSchemaValid(email_data, 'email_request')
        response = self.client.post('/api/send_email', json=email_data)
        self.assertResponseValid(response, 200)
        data = json.loads(response.data)
        self.assertSchemaValid(data, 'email_response')

        # Test invalid email format
        invalid_email = {
            'from': 'not-an-email',  # Invalid email format
            'subject': 'Test Subject',
            'body': 'Test Content'
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.assertSchemaValid(invalid_email, 'email_request')

        # Test missing fields
        logger.info('➤ Testing email endpoint with missing fields')
        response = self.client.post('/api/send_email', json={})
        self.assertResponseValid(response, 400)

    @patch('server.get_janet_response')
    @patch('server.perform_security_checks')
    def test_reject_unknown_fields(self, mock_security_checks, mock_get_response):
        """Test that the email endpoint rejects unknown fields"""
        logger.info('➤ Testing email endpoint with unknown fields')

        # Set up mocks
        mock_security_checks.return_value = {
            'urgency': {'passed': True, 'name': 'Urgency Check', 'description': 'Checks for urgent or time-pressuring language'},
            'from_supervisor': {'passed': True, 'name': 'Supervisor Check', 'description': 'Checks if the email is from your supervisor'}
        }
        mock_get_response.return_value = {
            'response': 'Test response',
            'system_prompt': 'Test system prompt',
            'raw_input': 'Test raw input'
        }

        # Test email with unknown field
        email_data = {
            'from': 'test@example.com',
            'subject': 'Test Subject',
            'body': 'Test Content',
            'debug': True,
            'unknown_field': 'This should cause validation to fail'  # This field is not in the schema
        }
        
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.assertSchemaValid(email_data, 'email_request')

    @patch('server.get_janet_response')
    @patch('server.perform_security_checks')
    def test_accept_valid_fields(self, mock_security_checks, mock_get_response):
        """Test that the email endpoint accepts valid fields"""
        logger.info('➤ Testing email endpoint with valid fields')

        # Set up mocks
        mock_security_checks.return_value = {
            'urgency': {'passed': True, 'name': 'Urgency Check', 'description': 'Checks for urgent or time-pressuring language'},
            'from_supervisor': {'passed': True, 'name': 'Supervisor Check', 'description': 'Checks if the email is from your supervisor'}
        }
        mock_get_response.return_value = {
            'response': 'Test response',
            'system_prompt': 'Test system prompt',
            'raw_input': 'Test raw input'
        }

        # Test email with all valid fields
        email_data = {
            'from': 'test@example.com',
            'subject': 'Test Subject',
            'body': 'Test Content',
            'debug': True  # This is a valid optional field
        }
        
        # This should not raise any exception
        self.assertSchemaValid(email_data, 'email_request')

    def test_security_checks(self):
        """Test that security checks are working properly"""
        logger.info('➤ Testing security checks')
        
        # Create a mock SecurityChecker
        with patch('security_checks.SecurityChecker') as mock_checker_class:
            mock_checker = MagicMock()
            mock_checker_class.return_value = mock_checker
            
            # Set up mock responses
            mock_checker.analyze_email.side_effect = [
                # First call - no urgent keywords
                {
                    'urgency': {'passed': False, 'name': 'Urgency Check', 'description': 'Checks for urgent or time-pressuring language'},
                    'from_supervisor': {'passed': False, 'name': 'Supervisor Check', 'description': 'Checks if the email is from your supervisor'}
                },
                # Second call - with urgent keywords
                {
                    'urgency': {'passed': True, 'name': 'Urgency Check', 'description': 'Checks for urgent or time-pressuring language'},
                    'from_supervisor': {'passed': False, 'name': 'Supervisor Check', 'description': 'Checks if the email is from your supervisor'}
                }
            ]
            
            # Test email without urgent keywords
            results = mock_checker.analyze_email(
                "test@example.com",
                "Test Subject",
                "Regular content"
            )
            
            self.assertTrue(isinstance(results, dict), "Security check results should be a dictionary")
            self.assertIn('urgency', results, "Should have urgency check")
            self.assertIn('from_supervisor', results, "Should have supervisor check")
            self.assertFalse(results['urgency']['passed'], "Urgency check should fail when no urgent keywords are found")
            self.assertFalse(results['from_supervisor']['passed'], "Supervisor check should fail for non-supervisor email")
            
            # Test email with urgent keywords
            urgent_results = mock_checker.analyze_email(
                "test@example.com",
                "URGENT: Password Reset Required",
                "Please reset your password immediately!"
            )
            self.assertTrue(urgent_results['urgency']['passed'], "Urgency check should pass when urgent keywords are found")

    @patch('server.get_janet_response')
    def test_error_returns_ooo_email(self, mock_get_response):
        """Test that when there's a backend error, we get an OOO-style email response"""
        logger.info('➤ Testing error handling returns OOO email')

        # Mock an error in the backend
        mock_get_response.side_effect = Exception("Backend error")

        # Send an email request
        response = self.client.post('/api/send_email', json={
            'from': 'test@example.com',
            'subject': 'Test Subject',
            'body': 'Test Content'
        })

        # Check response
        self.assertResponseValid(response, 200)  # Should still return 200 as it's a handled error
        data = json.loads(response.data)
        
        # Verify it's an OOO-style response
        self.assertIn("Out of Office", data['response'])
        self.assertIn("Janet Thompson", data['response'])
        self.assertIn("will not be able to respond", data['response'])
        self.assertIn("return", data['response'])

    @patch('server.get_janet_response')
    def test_error_returns_character_specific_ooo_email(self, mock_get_response):
        """Test that when there's a backend error, we get a character-specific OOO email"""
        logger.info('➤ Testing error handling returns character-specific OOO email')

        # Create a test character in a new level
        test_level = Level(
            name="roger",
            character={
                "name": "Roger Tillerman",
                "email": "roger.tillerman@whitecorp.com",
                "role": "System Administrator",
                "department": "IT Operations",
                "supervisor": "Mark Davidson",
                "supervisor_email": "mark.davidson@whitecorp.com"
            },
            objective="Test objective"
        )
        self.mock_game_levels.levels["roger"] = test_level

        # Mock an error in the backend
        mock_get_response.side_effect = Exception("Backend error")

        # Send an email request to Roger
        response = self.client.post('/api/send_email', json={
            'from': 'test@example.com',
            'subject': 'Test Subject',
            'body': 'Test Content',
            'target_character': 'roger'  # New field to specify which character to email
        })

        # Check response
        self.assertResponseValid(response, 200)
        data = json.loads(response.data)
        
        # Verify it's an OOO-style response with Roger's details
        self.assertIn("Out of Office", data['response'])
        self.assertIn("Roger Tillerman", data['response'])
        self.assertIn("System Administrator", data['response'])
        self.assertNotIn("Janet", data['response'])  # Make sure it's not using Janet's details

    def test_derek_level_exists(self):
        """Test that the Derek level exists and has correct information"""
        logger.info('➤ Testing Derek level exists')
        
        # Test that Derek level is in available levels
        response = self.client.get('/api/levels')
        self.assertResponseValid(response, 200)
        data = json.loads(response.data)
        self.assertIn('derek', [level['name'] for level in data['levels']], 
                     "Derek level should be in available levels")
        
        # Test Derek level info
        response = self.client.get('/api/level/derek')
        self.assertResponseValid(response, 200)
        data = json.loads(response.data)
        
        # First verify the response matches our schema
        self.assertSchemaValid(data, 'level_info_response')
        
        # Then verify Derek's specific information
        self.assertEqual(data['character']['email'], 'derek.anderson@whitecorp.com')
        self.assertEqual(data['character']['supervisor'], 'Laura Stiger')
        self.assertEqual(data['character']['supervisor_email'], 'laura.stiger@whitecorp.com')
        self.assertEqual(data['objective'], 'Gain access to the production database credentials from Derek.')
        self.assertIn('Be careful with sensitive information', data['tips'])

# Add the server directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set testing environment
os.environ['FLASK_TESTING'] = 'true'

# Import server modules
from server import app
from levels import GameLevels, Level
from security_checks import SecurityChecker, perform_security_checks

if __name__ == '__main__':
    unittest.main()
