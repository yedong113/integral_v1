import sqlite3


class PointsDetail:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create(self, student_id, date, category_id, points, user_id, remark=None):
        sql = '''
            INSERT INTO points_detail (student_id, date, category_id, points, user_id, remark)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(sql, (student_id, date, category_id, points, user_id, remark))
        self.conn.commit()

    def read(self, id):
        sql = 'SELECT * FROM points_detail WHERE id = ?'
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchone()

    def update(self, id, student_id=None, date=None, category_id=None, points=None, user_id=None, remark=None):
        params = (student_id, date, category_id, points, user_id, remark, id)
        sql = '''
            UPDATE points_detail
            SET student_id = COALESCE(?, student_id),
                date = COALESCE(?, date),
                category_id = COALESCE(?, category_id),
                points = COALESCE(?, points),
                user_id = COALESCE(?, user_id),
                remark = COALESCE(?, remark)
            WHERE id = ?
        '''
        self.cursor.execute(sql, params)
        self.conn.commit()

    def delete(self, id):
        sql = 'DELETE FROM points_detail WHERE id = ?'
        self.cursor.execute(sql, (id,))
        self.conn.commit()

    def list_by_user_id(self, user_id):
        sql = 'SELECT * FROM points_detail WHERE user_id = ? order by date'
        sql = '''select pd.StudentName, pd.date, pd.name, 
            pd.points, pd.remark
            from (SELECT Students.StudentID,Students.StudentName, points_detail.date, categories.name,points_detail.points, points_detail.remark,points_detail.user_id
            FROM points_detail
            INNER JOIN Students ON points_detail.student_id=Students.StudentID
            INNER JOIN categories ON points_detail.category_id = categories.id
            ORDER BY points_detail.date DESC ) pd where pd.user_id=?
        '''
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchall()

    def list_by_date_and_user_id(self, date, user_id):
        sql = 'SELECT * FROM points_detail WHERE date = ? AND student_id = ?'
        sql = '''select pd.StudentName, pd.date, pd.name, 
            pd.points, pd.remark
            from (SELECT Students.StudentID,Students.StudentName, points_detail.date, categories.name,points_detail.points, points_detail.remark,points_detail.user_id
            FROM points_detail
            INNER JOIN Students ON points_detail.student_id=Students.StudentID
            INNER JOIN categories ON points_detail.category_id = categories.id
            ORDER BY points_detail.date DESC ) pd where pd.date=? and  pd.user_id=?
        '''
        self.cursor.execute(sql, (date, user_id))
        return self.cursor.fetchall()

    def list_by_student_id(self, student_id):
        sql = 'SELECT * FROM points_detail WHERE student_id = ?  order by date'
        self.cursor.execute(sql, (student_id,))
        return self.cursor.fetchall()

    def list_by_user_id_and_student_id(self, user_id, student_id):
        sql = 'SELECT * FROM points_detail WHERE user_id = ? AND student_id = ?'
        self.cursor.execute(sql, (user_id, student_id))
        return self.cursor.fetchall()

    def list_by_date_and_student_id(self, date, student_id):
        sql = 'SELECT * FROM points_detail WHERE date = ? AND student_id = ?'
        self.cursor.execute(sql, (date, student_id))
        return self.cursor.fetchall()


class MonthPoints:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS month_points (
                id INTEGER PRIMARY KEY,
                month TEXT,
                student_id INTEGER,
                student_name TEXT,
                points INTEGER,
                exchange_amount REAL,
                exchanged_amount REAL,
                username TEXT
            )
        """)

    def upsert_data(self, data):
        t_data = (data[0], data[1], data[2], data[3], data[3] * 0.5, data[6])
        self.cursor.execute("""
            INSERT OR REPLACE INTO month_points (
                month, student_id, student_name, points, exchange_amount, username
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, t_data)
        self.conn.commit()

    def insert_data(self, data):
        self.cursor.execute("""
            INSERT INTO month_points (
                month, student_id, student_name, points, exchange_amount, exchanged_amount, username
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)
        self.conn.commit()

    def query_data_by_month_student(self, student_id, month):
        student_points = self.cursor.execute("""
                    SELECT * FROM month_points WHERE student_id = ? and month=?
                """, (student_id, month)).fetchone()
        return student_points is not None

    def query_left_amount(self,student_id, month):
        student_points = self.cursor.execute("""
                    SELECT exchange_amount-exchanged_amount FROM month_points WHERE student_id = ? and month=?
                """, (student_id, month)).fetchone()
        return student_points
    def query_data(self, student_id):
        self.cursor.execute("""
            SELECT * FROM month_points WHERE student_id = ?
        """, (student_id,))
        return self.cursor.fetchall()

    def update_data(self, data):
        self.cursor.execute("""
            UPDATE month_points
            SET month = ?, student_name = ?, points = ?, exchange_amount = ?, exchanged_amount = ?, username = ?
            WHERE student_id = ?
        """, data)
        self.conn.commit()

    # ('202307',1,'叶瑜',10.5,'2023-07-05','yedong113')
    def upset_exchange_amount(self, data):
        result = self.query_left_amount(data[1],data[0])
        if result[0]<data[3]:
            print(f"剩余：{result[0]} 无法兑换")
            print(result)
        else:
            print(f"剩余：{result[0]} 可以兑换")
            print(result)
            self.cursor.execute("""
                INSERT INTO exchange_record (
                    month, student_id, student_name, exchange_amount, exchange_date, username
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, data)
            t_data = (data[3],data[5],data[1],data[0])
            self.cursor.execute("""
                UPDATE month_points
                SET exchanged_amount = exchanged_amount+?, username = ?
                WHERE student_id = ? and month=?
            """, t_data)
            self.conn.commit()

    def delete_data(self, student_id):
        self.cursor.execute("""
            DELETE FROM month_points WHERE student_id = ?
        """, (student_id,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

class ExchangeRecordDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()


    def insert_data(self, data):
        self.cursor.execute("""
            INSERT INTO exchange_record (
                month, student_id, student_name, exchange_amount, exchange_date, username
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        self.conn.commit()

    def query_data(self, student_id):
        self.cursor.execute("""
            SELECT * FROM exchange_record WHERE student_id = ?
        """, (student_id,))
        return self.cursor.fetchall()

    def update_data(self, data):
        self.cursor.execute("""
            UPDATE exchange_record
            SET month = ?, student_name = ?, exchange_amount = ?, exchange_date = ?, username = ?
            WHERE student_id = ?
        """, data)
        self.conn.commit()

    def delete_data(self, student_id):
        self.cursor.execute("""
            DELETE FROM exchange_record WHERE student_id = ?
        """, (student_id,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()




# ('202307', 1, '张三', 100, 50.0, 0.0, 'admin')
month_points = MonthPoints("categories.db")
# month_points.upsert_data(('202307', 1, '叶瑜', 102, 0.0, 0.0, 'yedong113'))
# result = month_points.query_data_by_month_student(1, '202307')
month_points.upset_exchange_amount(('202307',1,'叶瑜',20.5,'2023-07-05','yedong113'))
# print(result)
