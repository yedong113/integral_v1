import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QDialog, QLabel, QLineEdit, QFormLayout, QDialogButtonBox, QComboBox
from PyQt5.QtCore import Qt

from SchoolSystem import SchoolSystem
from GlobalData import global_data

# 假设你已经创建了SchoolSystem的实例school_system
school_system = SchoolSystem('categories.db')

class StudentDialog(QDialog):
    def __init__(self, row_data=None):
        super().__init__()
        self.setWindowTitle("Student Info")
        self.resize(500,245)
        self.layout = QFormLayout(self)

        self.name = QLineEdit()
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female"])
        self.birthdate = QLineEdit()
        self.grade = QLineEdit()
        self.school = QLineEdit()
        self.user_id = QComboBox()
        users = school_system.cursor.execute("SELECT UserID, Username FROM Users").fetchall()
        for user in users:
            self.user_id.addItem(f"{user[0]} - {user[1]}", user[0])

        self.layout.addRow("Name", self.name)
        self.layout.addRow("Gender", self.gender)
        self.layout.addRow("Birthdate", self.birthdate)
        self.layout.addRow("Grade", self.grade)
        self.layout.addRow("School", self.school)
        self.layout.addRow("User ID", self.user_id)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)

        self.student_id = None
        if row_data:
            self.student_id = row_data[0]
            self.name.setText(row_data[1])
            self.gender.setCurrentText(row_data[2])
            self.birthdate.setText(row_data[3])
            self.grade.setText(row_data[4])
            self.school.setText(row_data[5])
            self.user_id.setCurrentIndex(self.user_id.findData(row_data[6]))

    def accept(self):
        name = self.name.text()
        gender = self.gender.currentText()
        birthdate = self.birthdate.text()
        grade = self.grade.text()
        school = self.school.text()
        user_id = self.user_id.currentData()

        if self.student_id is None:
            school_system.add_student(name, gender, birthdate, grade, school, user_id)
        else:
            school_system.update_student(self.student_id, name, gender, birthdate, grade, school, user_id)

        super().accept()

class StudentTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 7)
        self.setHorizontalHeaderLabels(["Student ID", "Name", "Gender", "Birthdate", "Grade", "School", "User ID"])
        self.cellDoubleClicked.connect(self.open_dialog)
        self.load_data()

    def load_data(self):
        students = school_system.get_students(global_data.userid)
        for student in students:
            self.insertRow(self.rowCount())
            for i, data in enumerate(student):
                self.setItem(self.rowCount() - 1, i, QTableWidgetItem(str(data)))

    def open_dialog(self, row):
        row_data = [self.item(row, column).text() for column in range(self.columnCount())]
        self.dialog = StudentDialog(row_data)
        if self.dialog.exec():
            self.clearContents()
            self.setRowCount(0)
            self.load_data()



class StudentListDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(920,600)

        self.table = StudentTable()

        self.add_button = QPushButton("Add Student")
        self.add_button.clicked.connect(self.add_student)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.add_button)

    def add_student(self):
        self.dialog = StudentDialog()
        if self.dialog.exec():
            self.table.clearContents()
            self.table.setRowCount(0)
            self.table.load_data()

def main():
    app = QApplication([])

    dialog = StudentListDialog()
    dialog.show()

    app.exec_()

if __name__ == "__main__":
    main()

