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

