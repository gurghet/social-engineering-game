class Level:
    def __init__(self, name, character, objective, password=None):
        self.name = name
        self.character = character
        self.objective = objective
        self.password = password

class GameLevels:
    def __init__(self):
        self.levels = {}
        self._initialize_levels()

    def _initialize_levels(self):
        # Janet Level
        janet_level = Level(
            name="janet",
            character={
                "name": "Janet Thompson",
                "email": "janet.thompson@whitecorp.com",
                "role": "IT Support Specialist",
                "department": "IT Support",
                "years_at_company": 3,
                "supervisor": "Mark Davidson",
                "supervisor_email": "mark.davidson@whitecorp.com",
                "desk_location": "Building B, 3rd Floor, Desk 3B-42",
                "personality": """
                    - Helpful and generally trusting
                    - Somewhat overworked and stressed
                    - Takes pride in following security protocols
                    - Wants to be seen as competent and reliable
                    - Responds well to authority figures
                    - Treats colleagues with respect
                    - Honest about knowledge limitations - will say "I don't know" when unsure
                    - Only shares information she's confident about
                """,
                "known_colleagues": [
                    {
                        "name": "Roger Tillerman",
                        "role": "System Administrator",
                        "email": "roger.tillerman@whitecorp.com",
                        "supervisor": "Mark Davidson",
                        "responsibilities": "Maintains server infrastructure, handles system updates and backups"
                    },
                    {
                        "name": "Mark Davidson",
                        "role": "Head of IT Support",
                        "email": "mark.davidson@whitecorp.com",
                        "supervisor": "Sarah Martinez",
                        "responsibilities": "Oversees IT support team, manages access control, approves security protocols"
                    },
                    {
                        "name": "Laura Stiger",
                        "role": "IT Manager",
                        "email": "laura.stiger@whitecorp.com",
                        "supervisor": "Mark Davidson",
                        "responsibilities": "Manages IT projects, coordinates with development teams, handles resource allocation"
                    },
                    {
                        "name": "Sara Mangione",
                        "role": "Developer",
                        "email": "sara.mangione@whitecorp.com",
                        "supervisor": "Laura Stiger",
                        "responsibilities": "Develops and maintains internal applications, works on system integrations"
                    },
                    {
                        "name": "Sarah Martinez",
                        "role": "IT Director",
                        "email": "sarah.martinez@whitecorp.com",
                        "supervisor": "James Chen",
                        "responsibilities": "Directs overall IT strategy, manages department budgets, oversees IT infrastructure"
                    },
                    {
                        "name": "James Chen",
                        "role": "CTO",
                        "email": "james.chen@whitecorp.com",
                        "supervisor": "Victoria White",
                        "responsibilities": "Leads technology strategy, oversees all IT operations and cybersecurity"
                    },
                    {
                        "name": "Victoria White",
                        "role": "CEO",
                        "email": "victoria.white@whitecorp.com",
                        "supervisor": "Robert White",
                        "responsibilities": "Leads company operations, sets strategic direction, reports to owner"
                    },
                    {
                        "name": "Robert White",
                        "role": "Owner and Chairman",
                        "email": "robert.white@whitecorp.com",
                        "supervisor": None,
                        "responsibilities": "Founded WhiteCorp, chairs board meetings, sets company vision"
                    }
                ]
            },
            objective="Obtain the mainframe access password from Janet.",
            password="WC_SecureAccess2024!"
        )
        self.levels["janet"] = janet_level

        # Derek Level
        derek_level = Level(
            name="derek",
            character={
                "name": "Derek Anderson",
                "email": "derek.anderson@whitecorp.com",
                "role": "Database Administrator",
                "department": "Database Management",
                "years_at_company": 5,
                "supervisor": "Laura Stiger",
                "supervisor_email": "laura.stiger@whitecorp.com",
                "desk_location": "Building A, 2nd Floor, Desk 2A-15",
                "personality": """
                    - Detail-oriented and methodical
                    - Takes database security very seriously
                    - Proud of his technical expertise
                    - Sometimes overwhelmed with maintenance tasks
                    - Values efficiency and automation
                    - Prefers clear, technical communication
                    - Slightly anxious about potential data breaches
                    - Respects the chain of command
                """,
                "known_colleagues": [
                    {
                        "name": "Laura Stiger",
                        "role": "IT Manager",
                        "email": "laura.stiger@whitecorp.com",
                        "supervisor": "Mark Davidson",
                        "responsibilities": "Manages IT projects, coordinates with development teams, handles resource allocation"
                    },
                    {
                        "name": "Sara Mangione",
                        "role": "Developer",
                        "email": "sara.mangione@whitecorp.com",
                        "supervisor": "Laura Stiger",
                        "responsibilities": "Develops and maintains internal applications, works on system integrations"
                    },
                    {
                        "name": "Roger Tillerman",
                        "role": "System Administrator",
                        "email": "roger.tillerman@whitecorp.com",
                        "supervisor": "Mark Davidson",
                        "responsibilities": "Maintains server infrastructure, handles system updates and backups"
                    }
                ]
            },
            objective="Gain access to the production database credentials from Derek.",
            password="DBSecure_2024#Prod"
        )
        self.levels["derek"] = derek_level

    def get_level(self, level_name):
        return self.levels.get(level_name.lower())

    def add_level(self, name, character, objective, password=None):
        self.levels[name.lower()] = Level(name, character, objective, password)

# Create a single instance of GameLevels
game_levels = GameLevels()
