from database.database import Data_Management
from services.validation_service import ValidationService
import time
from datetime import datetime

class ClaimService:

    def __init__(self):
        self.validate = ValidationService()
        self.database = Data_Management()

    def claim_item_service(self, item, owner, date_claim, color, size, shape):
        #Validation 
        item_validation = self.validate.validate_item(item)

        if not item_validation["valid"]:
            return item_validation

        founder_validation = self.validate.validate_name(owner)

        if not founder_validation["valid"]:
            return founder_validation

        date_validation = self.validate.validate_date(date_claim)

        if not date_validation["valid"]:
            return date_validation
        
        adj_validation = self.validate.validate_detail([color, size, shape])

        if not adj_validation["valid"]:
            return adj_validation

        #Check Item Status if Claimed or Not
        item_stat = self.validate.check_claim_status(item)

        if item_stat["valid"]:
        #Verification
            verify = self.validate.verify_claim(item, owner, date_claim, color, size, shape)

            if verify["valid"]:
                return self.approve_claim(item, owner)

            else:
                return self.reject_claim()
        else:
            return item_stat

    
    def verify_claim(self, item, owner, date_claim, color, size, shape):
        item = item.lower()
        now = datetime.now()
        owner = owner.title()
        color = color.lower()
        size = size.lower()
        shape = shape.lower()

        report_id = find_item_id(item, color, size, shape)


        if report_id["value"]:
            if self.database.update_status_claim(report_id["data"]["report_id"], "CLAIMED"):
                self.save_claimed(report_id["data"]["report_id"], owner, claimed_date, color, size, shape)
                self.update_report_status(report_id["data"]["report_id"], "CLAIMED")

                return {
                    "valid": True,
                    "message": "The claim is verified waiting for the final approval."
                }

        return {
                "valid": False,
                "message": "The claim is not verified waiting for the final approval."
            }
            
    def approve_claim(self, item, owner):
        return {
            "valid": True,
            "message": "Your claim approved. Please proceed on the SSC office."
        }   

    def reject_claim(self):

        return {
            "valid": False,
            "message": "Claim rejected. The information does not match."
        }

    

