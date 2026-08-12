from models.system import School_LostFound
from database.database import Data_Management


class Admin(School_LostFound, Data_Management):
    def __init__(self, item=None, date_found=None, date_return=None, founder=None, owner=None):
        super().__init__(item, date_found, date_return, founder, owner)
