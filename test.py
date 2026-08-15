from database.database import Data_Management
from datetime import datetime

db = Data_Management()

db.save_claimed(4, "Alcanara, Lyka", datetime.now(), "Black", "Small", "Rectangle")