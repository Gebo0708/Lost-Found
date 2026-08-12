from database.database import Data_Management
from services.validation_service import ValidationService
from services.claim_service import ClaimService

DATABASE_FILE = "database/items.json"

class ReportService:
    def __init__(self):
        self.validate = ValidationService()

    def report_lost_item_service(self, item, founder, date_found):

        item_validation = self.validate.validate_item(item)

        if not item_validation["valid"]:
            return item_validation

        founder_validation = self.validate.validate_name(founder)

        if not founder_validation["valid"]:
            return founder_validation

        date_validation = self.validate.validate_date(date_found)

        if not date_validation["valid"]:
            return date_validation
        
        ad = Data_Management()

        dup_validation = self.validate.check_duplicate(item, founder, date_found)

        if not dup_validation["valid"]:
            return dup_validation

        ad.save_data(item, date_found, founder, False, None, None)
        
        return {
            "valid": True,
            "message": "Thank you for returning the item."
        }
                

    def claim_item_service(self, item, owner, date_claim):
        c = ClaimService()
        res = c.claim_item_service(item, owner, date_claim) 
        return res