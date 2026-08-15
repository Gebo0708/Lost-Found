import mysql.connector

class Data_Management:

    def connect(self):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='18_gabriel',
            database='lost_found'
        )

        return connection
    
    
    def update_report_status(self, report_id, status):
        connection = self.connect()
        cursor = connection.cursor()

        sql = """UPDATE reports 
        SET status = %s
        WHERE report_id = %s"""

        cursor.execute(sql, (status, report_id))

        connection.commit()

        cursor.close()
        connection.close()

        print("Update Successfully.")

    def load_reports(self):

        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reports")

        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data

    def save_report(self, item, founder, date_found, color, size, shape):
        connection = self.connect()
        cursor = connection.cursor()

        sql = """
            INSERT INTO reports 
            (item, founder, date_found, color, size, shape)
            VALUES
            (%s, %s, %s, %s, %s, %s)
        """

        values = (
            item, 
            founder, 
            date_found, 
            color, 
            size, 
            shape
        )

        cursor.execute(sql, values)

        connection.commit()

        cursor.close()
        connection.close()

        print("Report Saved Successfully.")

    def save_claimed(self, report_id, owner, claimed_date, color, size, shape):

        connection = self.connect()
        cursor = connection.cursor()
        
        sql = """
            INSERT INTO claims
            (report_id, owner, claimed_date, color, size, shape)
            VALUES
            (%s, %s, %s, %s, %s, %s)
        """
        values = (report_id, owner, claimed_date, color, size, shape)

        cursor.execute(sql, values)

        connection.commit()

        cursor.close()
        connection.close()

        print("Claimed Saved Successfully.")

    def load_claims(self):

        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM claims")

        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data

    def update_claim_status(self, report_id, status):
        connection = self.connect()
        cursor = connection.cursor()

        sql = """
            UPDATE claims
            SET status = %s
            WHERE report_id = %s        
        """
        cursor.execute(sql, (status, report_id))

        connection.commit()

        cursor.close()
        connection.close()

        print("Claim Updated Successfully.")    

# import os
# import time
# from datetime import datetime
# import json

# DATABASE_FILE = "database/items.json"

# class Data_Management:

#     def create_dict(self, item, date_found, founder, status,  color, size, shape, owner=None, d_found=None):
#         item = item.lower()
#         founder = founder.title()
#         color = color.lower()
#         size = size.lower()
#         shape = shape.lower()
#         load_data = self.load_data()
#         id_n = len(load_data) + 1
#         data_dict = {
#             id_n:
#             {"item": item, 
#             "date_found":date_found, 
#             "founder":founder, 
#             "status":status, "owner":owner, 
#             "d_return":d_found, 
#             "color": color,
#             "size": size,
#             "shape": shape
#             }
#         }

#         return data_dict

#     def save_data(self, item, date_found, founder, status, color, size, shape, owner=None, d_found=None):
#         data_dict = self.create_dict(item, date_found, founder, status, color, size, shape, owner, d_found)

#         if os.path.exists(DATABASE_FILE):
#             with open(DATABASE_FILE, "r") as file:
#                 load = json.load(file)

#             load.update(data_dict)

#             with open(DATABASE_FILE, "w") as file:
#                 json.dump(load, file, indent=4)

#     def save_item(self, data):
#         if os.path.exists(DATABASE_FILE):
#             with open(DATABASE_FILE, "w") as file:
#                 json.dump(data, file, indent=4)

#     def load_data(self):
#         if os.path.exists(DATABASE_FILE):
#             with open(DATABASE_FILE, "r") as file:
#                 loaded_data = json.load(file)
#                 return loaded_data