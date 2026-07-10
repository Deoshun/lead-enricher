from enrich.search import search
from enrich.scrape import Scraper
from lead.lead import EnrichedLead

class Contact():
    def __init__(self, name, address, website = ''):
        self.website = website
        self.name = name
        self.address = address
        self.socials = set()
        self.phones = set()
        self.emails = set()

    def missing_fields(self):
        return not (self.emails and self.socials and self.phones)

    def update(self, data):
        print('updating contact')
        print(data)
        extracted_emails = data['emails']
        extracted_socials = data['socials']
        extracted_phones = data['phones']
        tictok_links = []
        instagram_links = []

        self.emails.update(extracted_emails)
        self.phones.update(extracted_phones)
        self.socials.update(extracted_socials)

class ContactFinder():
    def __init__(self):
        self.search = search 
        self.scraper = Scraper() 

    def find(self, lead):
        contact = Contact(lead.company_name, lead.address, lead.website)
        if lead.website:
            print(lead.website)
            extracted_data = self.scraper.extract_static(lead.website)
            print(extracted_data)
            contact.update(extracted_data)

        if contact.missing_fields:
            print('Missing infomation, running search')
            results = search(lead.company_name + ' ' + lead.address, 3)
            for link in results:
                if contact.missing_fields:
                    data = self.scraper.extract_static(link)
                    contact.update(data)
        return contact

class Enrich:
    def __init__(self):
        self.contact_finder = ContactFinder()

    def enrich_lead(self, lead):
        aquired_contact_infomation = self.contact_finder.find(lead)
        return EnrichedLead(lead, aquired_contact_infomation)

    def enrich_leads(self, leads):
        enriched_leads = []
        for lead in leads:
            enriched_lead = self.enrich_lead(lead)
            enriched_leads.append(enriched_lead)
        return enriched_leads
