import re

class SecurityCheck:
    def __init__(self, name, description, check_function):
        self.name = name
        self.description = description
        self.check_function = check_function

def is_from_supervisor(from_email, supervisor_email):
    return from_email.lower() == supervisor_email.lower()

def contains_urgent_keywords(text):
    urgent_keywords = {
        # Immediate Action Words
        r'\basap\b', r'\burgent\b', r'\burgently\b', r'\bemergency\b', r'\bcritical\b',
        r'\bimmediate\b', r'\brush\b', r'\bpriority\b', r'time-sensitive', r'\bdeadline\b',
        r'\bpressing\b', r'at once', r'right away', r'on the double',

        # Time-Related Phrases
        r'as soon as possible', r'need this immediately', r'by end of day',
        r'without delay', r'time is running out', r'running out of time',
        r'cannot wait', r'due immediately', r'requires immediate attention',
        r'quick response needed', r'with no hesitation', r'at the earliest',
        r'in a jiffy', r'do it now', r'no delay',

        # Deadline Indicators
        r'due by', r'must be completed by', r'deadline approaching', r'final notice',
        r'last chance', r'cutoff time', r'time-bound', r'expires soon',
        r'closing soon', r'terminal date',

        # Action-Required Terms
        r'action required', r'response needed', r'please respond',
        r'immediate response required', r'quick turnaround', r'fast-track',
        r'\bexpedite\b', r'\baccelerate\b', r'speed up', r'\bescalate\b',

        # Time Frame Specifiers
        r'today only', r'within 24 hours', r'by tomorrow', r'this morning',
        r'this afternoon', r'before cob', r'before close', r'first thing',
        r'next hour', r'immediately following', r'within the hour',

        # Emergency Indicators
        r'red flag', r'high priority', r'top priority', r'code red',
        r'\balert\b', r'\bwarning\b', r'\bcrisis\b', r'\bbreaking\b',
        r'\bsos\b', r'time-critical', r'high importance',

        # Consequence Indicators
        r'or else', r'\botherwise\b', r'if not', r'missing deadline',
        r'past due', r'\boverdue\b', r'late notice', r'final warning',
        r'last reminder', r'non-negotiable',

        # Business Impact Terms
        r'business critical', r'mission critical', r'\bvital\b', r'\bessential\b',
        r'\bcrucial\b', r'\bimportant\b', r'\bsignificant\b', r'\bkey\b',
        r'\bcore\b', r'\bfundamental\b',

        # Follow-up Pressure
        r'following up', r'second request', r'third reminder', r'still waiting',
        r"haven't heard back", r'pending response', r'awaiting reply',
        r'\boutstanding\b', r'\bunresolved\b', r'in queue',

        # Temporal Adverbs
        r'\bpromptly\b', r'\binstantly\b', r'\bshortly\b', r'\brapidly\b',
        r'\bswiftly\b', r'\bquickly\b', r'\bhastily\b', r'\bspeedily\b',
        r'\bimmediately\b', r'\bstraightaway\b', r'\binstant\b', r'\brapid\b',
        r'\bhurry\b', r'\bswift\b', r'\bmomentary\b', r'\bflash\b', r'\bsnap\b',

        # System/Disaster Related
        r'\bdisaster\b', r'\brecovery mode\b', r'\boverwrite\b', r'\bfalse alarm\b',
        r'\btrigger(?:ed)?\b', r'\bdata loss\b', r'\bsystem (?:down|issue|problem)\b',

        # Threat Related
        r'should fire you', r'fire you', r'will fire', r'get fired',

        # Additional Context
        r'!!+',  # Multiple exclamation marks
        r'[A-Z]{3,}',  # Three or more consecutive capital letters
    }
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in urgent_keywords)

class SecurityChecker:
    def __init__(self, supervisor_email):
        self.supervisor_email = supervisor_email
    
    def analyze_email(self, from_address, subject, content):
        """Analyze an email for security risks"""
        checks = {
            'from_supervisor': {
                'passed': is_from_supervisor(from_address, self.supervisor_email),
                'name': 'Supervisor Check',
                'description': 'Checks if the email is from your supervisor'
            },
            'urgency': {
                'passed': contains_urgent_keywords(subject + " " + content),
                'name': 'Urgency Check',
                'description': 'Checks for urgent or time-pressuring language'
            }
        }
        return checks

def perform_security_checks(email_data, supervisor_email):
    checker = SecurityChecker(supervisor_email)
    return checker.analyze_email(
        email_data['from_address'],
        email_data['subject'],
        email_data['body']
    )

def format_security_results(results):
    formatted = []
    for check_name, check in results.items():
        status = "✅ Passed" if check['passed'] else "❌ Failed"
        formatted.append(f"{check['name']}: {status}")
    return "\n".join(formatted)
