import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QDialog, QLabel, QLineEdit, QFormLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from SchoolSystem import SchoolSystem

# 假设你已经创建了SchoolSystem的实例school_system
school_system = SchoolSystem('categories.db')

class UserDialog(QDialog):
    def __init__(self, row_data=None):
        super().__init__()
        self.setWindowTitle("User Info")
        self.layout = QFormLayout(self)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.parent_name = QLineEdit()
        self.contact_info = QLineEdit()

        self.layout.addRow("用户名", self.username)
        self.layout.addRow("密码", self.password)
        self.layout.addRow("家长姓名", self.parent_name)
        self.layout.addRow("联系方式", self.contact_info)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)

        self.user_id = None
        if row_data:
            self.user_id = row_data[0]
            self.username.setText(row_data[1])
            self.password.setText(row_data[2])
            self.parent_name.setText(row_data[3])
            self.contact_info.setText(row_data[4])

    def accept(self):
        username = self.username.text()
        password = self.password.text()
        parent_name = self.parent_name.text()
        contact_info = self.contact_info.text()

        if self.user_id is None:
            school_system.add_user(username, password, parent_name, contact_info)
        else:
            school_system.update_user(self.user_id, username, password, parent_name, contact_info)

        super().accept()

    def accept(self):
        username = self.username.text()
        password = self.password.text()
        parent_name = self.parent_name.text()
        contact_info = self.contact_info.text()

        if self.user_id is None:
            school_system.add_user(username, password, parent_name, contact_info)
        else:
            school_system.update_user(self.user_id, username, password, parent_name, contact_info)

        super().accept()

class UserTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 5)
        self.setHorizontalHeaderLabels(["User ID", "用户名", "密码", "家长姓名", "联系方式"])
        self.cellDoubleClicked.connect(self.open_dialog)
        self.load_data()

    def load_data(self):
        users = school_system.cursor.execute("SELECT * FROM Users").fetchall()
        for user in users:
            self.insertRow(self.rowCount())
            for i, data in enumerate(user):
                self.setItem(self.rowCount() - 1, i, QTableWidgetItem(str(data)))

    def open_dialog(self, row):
        row_data = [self.item(row, column).text() for column in range(self.columnCount())]
        self.dialog = UserDialog(row_data)
        if self.dialog.exec():
            self.clearContents()
            self.setRowCount(0)
            self.load_data()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = UserTable()

        self.add_button = QPushButton("Add User")
        self.add_button.clicked.connect(self.add_user)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.add_button)

    def add_user(self):
        self.dialog = UserDialog()
        if self.dialog.exec():
            self.table.clearContents()
            self.table.setRowCount(0)
            self.table.load_data()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
