class Character:
    def __init__(self, level_data):
        """Initialize a character from level data"""
        self.name = level_data["name"]
        self.email = level_data["email"]
        self.role = level_data["role"]
        self.department = level_data.get("department", "")
        self.supervisor = level_data.get("supervisor", "")
        self.supervisor_email = level_data.get("supervisor_email", "")
        self.knowledge = level_data

    def get_ooo_message(self):
        """Get an Out of Office message for this character"""
        department_contact = "helpdesk@whitecorp.com" if "IT" in self.department else f"{self.supervisor_email}"
        urgent_contact = f"For urgent {self.department} matters, please contact {department_contact}."

        return f"""Hi,

Thank you for your email. I am currently Out of Office and will not be able to respond to your request at this time. I will return to the office as soon as possible.

{urgent_contact}

Best regards,
{self.name}
{self.role}
WhiteCorp"""
