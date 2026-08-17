from database.database import Data_Management
from datetime import datetime

db = Data_Management()

data = db.find_item_id("Wallet", "Black", "Small", "Rectangle")["data"]["report_id"]

print(data) 