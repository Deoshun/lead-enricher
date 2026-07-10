import ast
from thefuzz import fuzz, process

class Lead():
    def __init__(self, name, address, types, phone, website = ''):
        self.qualified = 0
        self.score = 0
        self.processed = False
        self.company_name = name
        self.address = address
        self.website = ''
        self.types = []
        self.phone = phone
        if isinstance(website, str):
            self.website = website

        try:
            if isinstance(types, str) and types.startswith('['):
                self.types = ast.literal_eval(types)
            else:
                self.types = types
        except (ValueError, SyntaxError):
            self.types = []
    def to_dict(self):
            return self.__dict__

class EnrichedLead(Lead):
    def __init__(self, lead, aquired_data):
        self.__dict__.update(lead.to_dict())
        self.emails = aquired_data.emails
        self.main_email = process.extractOne(lead.company_name, list(aquired_data.emails))
        self.additional_numbers = aquired_data.phones
        self.socials = aquired_data.socials
