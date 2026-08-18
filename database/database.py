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

        return

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

        return

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

        return


    def load_claims(self):

        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM claims")

        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data

    # def update_claim_status(self, report_id, status):
    #     connection = self.connect()
    #     cursor = connection.cursor()

    #     sql = """
    #         UPDATE claims
    #         SET status = %s
    #         WHERE report_id = %s        
    #     """
    #     cursor.execute(sql, (status, report_id))

    #     connection.commit()

    #     cursor.close()
    #     connection.close()

    #     print("Claim Updated Successfully.") 

    def find_duplicate_report(self, item, name, date):
        connection = self.connect()
        cursor = connection.cursor()

        sql = """
            SELECT * FROM reports
            WHERE item = %s
            AND founder = %s
            AND date_found = %s
        """   
        cursor.execute(sql, (item, name, date))

        existed = bool(cursor.fetchone())

        if existed:
            return True
        
        return False

    def update_claim_status(self, report_id, status):
        connection = self.connect()
        cursor = connection.cursor()

        sql = """
            UPDATE claims 
            SET status = %s
            WHERE 
            report_id = %s
        """
        try:
            cursor.execute(sql, (status, report_id))
            connection.commit()

            return cursor.rowcount > 0
        
        except Exception as e:
            connection.rollback()

            return False
        
        finally:
            cursor.close()
            connection.close()

    def find_item_id(self, item, color, size, shape):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        sql = """
            SELECT report_id 
            FROM reports
            WHERE item = %s AND
            color = %s AND
            size = %s AND
            shape = %s AND
            status = "AVAILABLE"
        """

        cursor.execute(sql, (item, color, size, shape))

        find = bool(cursor.fetchone())
      

        cursor.close()
        connection.close()

        if find:
            return self.return_report_id(item, color, size, shape)

        return {
            "value": False,
            "data": None,
            "message": "Item cannot be found."
        }

    def return_report_id(self, item, color, size, shape):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        sql = """
            SELECT report_id 
            FROM reports
            WHERE item = %s AND
            color = %s AND
            size = %s AND
            shape = %s AND
            status = "AVAILABLE"
        """

        cursor.execute(sql, (item, color, size, shape))

        data = cursor.fetchone()
      

        cursor.close()
        connection.close()

        return {
            "value": True,
            "data": data
        }

    def check_status(self, report_id):
        connection = self.connect()
        cursor = connection.cursor()

        sql = """
            SELECT * FROM reports
            WHERE report_id = %s AND
            status = "AVAILABLE"
        """

        cursor.execute(sql, (report_id,))

        is_available = cursor.fetchone()

        cursor.close()
        connection.close()

        return bool(is_available)
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