from database.database import Data_Management
class ValidationService:

    def validate_item(self, item):
        if item != None:
            if isinstance(item, str):
                return {
                "valid": True,
                "message": "Valid item."
            }

        
        return {
        "valid": False,
        "message": "Invalid item."
    }

    def validate_detail(self, adjectives):
        for adj in adjectives:
            if adj != None:
                if isinstance(adj, str):
                    return {
                        "valid": True,
                        "message": "Valid Adjective"
                    }
        return {
                    "valid": False,
                    "message": "Invalid Adjective"
                }

    def validate_name(self, name):
        if name != None:
            if isinstance(name, str):
                return {
                    "valid": True,
                    "message": "Valid name."
                }

        return {
                    "valid": False,
                    "message": "Invalid name."
                }

    def validate_date(self, date):
        if date != None:
            year = date[:4]
            year = int(year)
            if year >= 2020 and year <= 2026:
                return {
                    "valid": True,
                    "message": "Valid Date."
                }
        return {
                    "valid": False,
                    "message": "Invalid Date."
                }

    def check_duplicate(self, item, name, date):
        ad = Data_Management()
        
        if ad.find_duplicate_report(item, name, date):
            return {
                "valid": False,
                "message": "Item Already Reported."
            }

        return {
                "valid": True,
                "message": "Reported Successfully"
            }    

    def check_claim_status(self, item):
        item_d = self.database.load_reports()
    
        #Validation
        for key in item_d:
            if item_d[key]["item"] == item:
                #Status Validation
                if item_d[key]["status"] == "AVAILABLE":
                    return {
                        "valid": True,
                        "message": "The Item is good. Proceeding."
                    }

                else:
                    return {
                        "valid": False,
                        "message": "The Item is already been claimed."

                    }
    
        return {
                "valid": False,
                "message": "The Item cannot be found. Try again."
            }
