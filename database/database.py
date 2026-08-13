import os
import time
from datetime import datetime
import json

DATABASE_FILE = "database/items.json"

class Data_Management:

    def create_dict(self, item, date_found, founder, status,  color, size, shape, owner=None, d_found=None):
        item = item.lower()
        founder = founder.title()
        color = color.lower()
        size = size.lower()
        shape = shape.lower()
        load_data = self.load_data()
        id_n = len(load_data) + 1
        data_dict = {
            id_n:
            {"item": item, 
            "date_found":date_found, 
            "founder":founder, 
            "status":status, "owner":owner, 
            "d_return":d_found, 
            "color": color,
            "size": size,
            "shape": shape
            }
        }

        return data_dict

    def save_data(self, item, date_found, founder, status, color, size, shape, owner=None, d_found=None):
        data_dict = self.create_dict(item, date_found, founder, status, color, size, shape, owner, d_found)

        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, "r") as file:
                load = json.load(file)

            load.update(data_dict)

            with open(DATABASE_FILE, "w") as file:
                json.dump(load, file, indent=4)

    def save_item(self, data):
        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, "w") as file:
                json.dump(data, file, indent=4)

    def load_data(self):
        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, "r") as file:
                loaded_data = json.load(file)
                return loaded_data