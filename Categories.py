import sqlite3

class Categories:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create(self, parent_id, name, default_points=None):
        if default_points is not None:
            sql = '''
                INSERT INTO categories (parent_id, name, default_points)
                VALUES (?, ?, ?)
            '''
            self.cursor.execute(sql, (parent_id, name, default_points))

        sql = '''
            INSERT INTO categories (parent_id, name)
            VALUES (?, ?)
        '''
        self.cursor.execute(sql, (parent_id, name))
        self.conn.commit()

    def read(self, id):
        sql = 'SELECT * FROM categories WHERE id = ?'
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchone()

    def getCategories(self, parent_id):
        if parent_id is None:
            self.cursor.execute('SELECT * FROM categories WHERE parent_id IS NULL')
        else:
            self.cursor.execute('SELECT * FROM categories WHERE parent_id=?', (parent_id,))
        return self.cursor.fetchall()

    def update(self, id, parent_id=None, name=None, default_points=None):
        params = (parent_id, name, default_points, id)
        sql = '''
            UPDATE categories
            SET parent_id = COALESCE(?, parent_id),
                name = COALESCE(?, name),
                default_points = COALESCE(?, default_points)
            WHERE id = ?
        '''
        self.cursor.execute(sql, params)
        self.conn.commit()

    def delete(self, id):
        sql = 'DELETE FROM categories WHERE id = ?'
        self.cursor.execute(sql, (id,))
        self.conn.commit()

    def list_all(self):
        sql = 'SELECT * FROM categories'
        self.cursor.execute(sql)
        return self.cursor.fetchall()
