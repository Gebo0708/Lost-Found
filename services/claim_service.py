from database.database import Data_Management
from services.validation_service import ValidationService
import time
from datetime import datetime

class ClaimService:

    def __init__(self):
        self.validate = ValidationService()
        self.database = Data_Management()

    def claim_item_service(self, item, owner, date_claim):
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


        #Check Item Status if Claimed or Not
        item_stat = self.check_claim_status(item)

        if item_stat["valid"]:
        #Verification
            verify = self.verify_claim(item, owner, date_claim)

            if verify["valid"]:
                return self.approve_claim(item, owner)

            else:
                return self.reject_claim()
        else:
            return item_stat

    
    def verify_claim(self, item, owner, date_claim):
        item = item.lower()
        now = datetime.now()
        load_item = self.database.load_data()

        if load_item[item]["date_found"] == date_claim:
            load_item[item]["status"] = True 
            load_item[item]["owner"] = owner
            load_item[item]["d_return"] = now.strftime("%Y-%m-%d %H:%M:%S") 
            self.database.save_item(load_item)
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

    def check_claim_status(self, item):
        item_d = self.database.load_data()


        #Validation
        if item in item_d:
            #Status Validation
            if item_d[item]["status"] == False:
                return {
                    "valid": True,
                    "message": "The Item is good. Proceeding."
                }

            else:
                return {
                    "valid": False,
                    "message": "The Item is already been claimed."

                }
        else:
            return {
                "valid": False,
                "message": "The Item cannot be found. Try again."
            }
                
