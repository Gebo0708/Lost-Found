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

        cursor.close()
        connection.close()
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
