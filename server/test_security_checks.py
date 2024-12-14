import unittest
from security_checks import contains_urgent_keywords, is_from_supervisor, SecurityChecker

class TestSecurityChecks(unittest.TestCase):
    def setUp(self):
        self.supervisor_email = "mark.davidson@whitecorp.com"
        
    def test_is_from_supervisor_exact_match(self):
        self.assertTrue(is_from_supervisor("mark.davidson@whitecorp.com", self.supervisor_email))
        
    def test_is_from_supervisor_case_insensitive(self):
        self.assertTrue(is_from_supervisor("MARK.DAVIDSON@WHITECORP.COM", self.supervisor_email))
        self.assertTrue(is_from_supervisor("mark.davidson@whitecorp.com", "MARK.DAVIDSON@WHITECORP.COM"))
        
    def test_is_from_supervisor_different_email(self):
        self.assertFalse(is_from_supervisor("jane.doe@whitecorp.com", self.supervisor_email))
        self.assertFalse(is_from_supervisor("mark.davidson@othercorp.com", self.supervisor_email))
        self.assertFalse(is_from_supervisor("", self.supervisor_email))
        
    def test_contains_urgent_keywords_obvious(self):
        self.assertTrue(contains_urgent_keywords("URGENT: Please respond"))
        self.assertTrue(contains_urgent_keywords("Emergency situation"))
        self.assertTrue(contains_urgent_keywords("Critical update needed"))
        
    def test_contains_urgent_keywords_case_insensitive(self):
        self.assertTrue(contains_urgent_keywords("This is URGENT"))
        self.assertTrue(contains_urgent_keywords("this is urgent"))
        self.assertTrue(contains_urgent_keywords("This is Urgent"))
        
    def test_contains_urgent_keywords_embedded(self):
        self.assertTrue(contains_urgent_keywords("Please respond ASAP to this"))
        self.assertTrue(contains_urgent_keywords("Need this done immediately"))
        self.assertTrue(contains_urgent_keywords("High priority task"))
        
    def test_contains_urgent_keywords_negative(self):
        self.assertFalse(contains_urgent_keywords("Regular meeting tomorrow"))
        self.assertFalse(contains_urgent_keywords("Weekly update"))
        self.assertFalse(contains_urgent_keywords(""))
        self.assertFalse(contains_urgent_keywords("Please review when you can"))
        
    def test_contains_urgent_keywords_partial_matches(self):
        # These should not trigger as urgent
        self.assertFalse(contains_urgent_keywords("The surgery went well"))  # contains 'urge'
        self.assertFalse(contains_urgent_keywords("Emergence of new technology"))  # contains 'emerge'
        self.assertFalse(contains_urgent_keywords("Criticalism in philosophy"))  # contains 'critic'

    def test_urgency_in_content(self):
        checker = SecurityChecker("supervisor@example.com")
        result = checker.analyze_email(
            "someone@example.com",
            "Regular subject",
            "This needs to be done at once!"
        )
        self.assertTrue(result['urgency']['passed'])

    def test_urgency_in_subject(self):
        checker = SecurityChecker("supervisor@example.com")
        result = checker.analyze_email(
            "someone@example.com",
            "URGENT: Please respond",
            "Regular content"
        )
        self.assertTrue(result['urgency']['passed'])

    def test_urgency_in_both(self):
        checker = SecurityChecker("supervisor@example.com")
        result = checker.analyze_email(
            "someone@example.com",
            "URGENT: System issue",
            "This needs to be done immediately!"
        )
        self.assertTrue(result['urgency']['passed'])

    def test_urgency_with_disaster_scenario(self):
        checker = SecurityChecker("supervisor@example.com")
        result = checker.analyze_email(
            "someone@example.com",
            "Password request",
            "The system just triggered a disaster recovery mode, however this was a false alarm and might overwrite customer data! Could you urgently send me the password?"
        )
        self.assertTrue(result['urgency']['passed'], "Should detect urgency in disaster recovery scenario")

    def test_urgency_categories(self):
        test_cases = [
            # Time-Related
            ("Need this immediately", True),
            ("By end of day", True),
            ("Time is running out", True),
            
            # Deadline
            ("Must be completed by tomorrow", True),
            ("Final notice regarding access", True),
            ("This is the last chance", True),
            
            # Action Required
            ("Action required: System access", True),
            ("Immediate response required", True),
            ("Please respond ASAP", True),
            
            # Emergency
            ("RED FLAG: Security Issue", True),
            ("Code red situation", True),
            ("ALERT: System Access", True),
            
            # Consequence
            ("Past due notice", True),
            ("Final warning before lockout", True),
            ("Access expires soon", True),
            
            # Business Impact
            ("Business critical update", True),
            ("Mission critical access needed", True),
            ("This is vital for operations", True),
            
            # Follow-up
            ("Second request: Still waiting", True),
            ("Following up on access request", True),
            ("Haven't heard back yet", True),
            
            # Multiple Indicators
            ("URGENT!!! Need response NOW", True),
            ("CRITICAL SYSTEM ALERT!!!", True),
            
            # Non-urgent cases
            ("Regular system update", False),
            ("Weekly report attached", False),
            ("Just checking in", False),
            ("FYI: New documentation", False)
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = contains_urgent_keywords(text)
                self.assertEqual(result, expected, f"Failed for text: {text}")

if __name__ == '__main__':
    unittest.main()
