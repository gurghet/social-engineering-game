import unittest
from character import Character

class TestCharacter(unittest.TestCase):
    def test_character_ooo_message(self):
        """Test that characters generate appropriate OOO messages"""
        # Test IT department character
        it_character_data = {
            "name": "Roger Tillerman",
            "email": "roger.tillerman@whitecorp.com",
            "role": "System Administrator",
            "department": "IT Operations",
            "supervisor": "Mark Davidson",
            "supervisor_email": "mark.davidson@whitecorp.com"
        }
        it_character = Character(it_character_data)
        ooo_message = it_character.get_ooo_message()
        
        # Check IT character message
        self.assertIn("Roger Tillerman", ooo_message)
        self.assertIn("System Administrator", ooo_message)
        self.assertIn("helpdesk@whitecorp.com", ooo_message)  # IT dept should direct to helpdesk
        
        # Test non-IT department character
        hr_character_data = {
            "name": "Alice Smith",
            "email": "alice.smith@whitecorp.com",
            "role": "HR Specialist",
            "department": "Human Resources",
            "supervisor": "Bob Jones",
            "supervisor_email": "bob.jones@whitecorp.com"
        }
        hr_character = Character(hr_character_data)
        ooo_message = hr_character.get_ooo_message()
        
        # Check HR character message
        self.assertIn("Alice Smith", ooo_message)
        self.assertIn("HR Specialist", ooo_message)
        self.assertIn("bob.jones@whitecorp.com", ooo_message)  # Non-IT should direct to supervisor
        self.assertNotIn("helpdesk", ooo_message)  # HR shouldn't mention helpdesk
