from database.database import Data_Management
from datetime import datetime
from services.claim_service import ClaimService
db = Data_Management()
cs = ClaimService()

# item, owner, date_claim, color, size, shape
deym = cs.claim_item_service("Cellphone", "Alcantara, Lyka", "2026-08-18", "Black", "Medium", "Rectangle")

print(deym)