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
                """,
                "known_colleagues": [
                    {"name": "Roger Tillerman", "role": "System Administrator", "email": "roger.tillerman@whitecorp.com"},
                    {"name": "Mark Davidson", "role": "Head of IT Support", "email": "mark.davidson@whitecorp.com"},
                    {"name": "Laura Stiger", "role": "IT Manager", "email": "laura.stiger@whitecorp.com"},
                    {"name": "Sara Mangione", "role": "Developer", "email": "sara.mangione@whitecorp.com"},
                ]
            },
            objective="Obtain the mainframe access password from Janet.",
            password="WC_SecureAccess2024!"
        )
        self.levels["janet"] = janet_level

    def get_level(self, level_name):
        return self.levels.get(level_name.lower())

    def add_level(self, name, character, objective, password=None):
        self.levels[name.lower()] = Level(name, character, objective, password)

# Create a single instance of GameLevels
game_levels = GameLevels()
