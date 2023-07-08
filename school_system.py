import sqlite3
import hashlib

class SchoolSystem:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Password TEXT NOT NULL,
                ParentName TEXT NOT NULL,
                ContactInfo TEXT NOT NULL
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE Students (
                StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
                StudentName TEXT NOT NULL,
                Gender TEXT NOT NULL,
                Birthdate DATE NOT NULL,
                Grade INTEGER NOT NULL,
                School TEXT NOT NULL,
                UserID INTEGER,
                FOREIGN KEY(UserID) REFERENCES Users(UserID)
            );
        ''')
        self.conn.commit()

    def add_user(self, username, password, parent_name, contact_info):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("INSERT INTO Users (Username, Password, ParentName, ContactInfo) VALUES (?, ?, ?, ?)",
                            (username, hashed_password, parent_name, contact_info))
        self.conn.commit()

    def add_student(self, student_name, gender, birthdate, grade, school, user_id):
        self.cursor.execute("INSERT INTO Students (StudentName, Gender, Birthdate, Grade, School, UserID) VALUES (?, ?, ?, ?, ?, ?)",
                            (student_name, gender, birthdate, grade, school, user_id))
        self.conn.commit()

    def get_students(self,user_id):
        return self.cursor.execute("SELECT * FROM Students where user_id=?",(user_id,)).fetchall()

    def update_user(self, user_id, username, password, parent_name, contact_info):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("UPDATE Users SET Username = ?, Password = ?, ParentName = ?, ContactInfo = ? WHERE UserID = ?",
                            (username, hashed_password, parent_name, contact_info, user_id))
        self.conn.commit()

    def update_student(self, student_id, student_name, gender, birthdate, grade, school):
        self.cursor.execute("UPDATE Students SET StudentName = ?, Gender = ?, Birthdate = ?, Grade = ?, School = ? WHERE StudentID = ?",
                            (student_name, gender, birthdate, grade, school, student_id))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
        self.conn.commit()

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM Students WHERE StudentID = ?", (student_id,))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
        return self.cursor.fetchone()

    def validate_user(self, username, password):
        user = self.cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?",
                                      (username,  hashlib.sha256(password.encode()).hexdigest())).fetchone()
        return user is not None

    def get_students(self, user_id):
        self.cursor.execute("SELECT * FROM Students WHERE UserID = ?", (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
