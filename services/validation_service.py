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
        data = ad.load_data()

        for key in data:
            if key == item and data[key]["founder"] == name and data[key]["date_found"] == date:
                return {
                    "valid": False,
                    "message": "Item Already Reported."
                }

        return {
                "valid": True,
                "message": "Reported Successfully"
            }    