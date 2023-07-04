import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QPushButton, QWidget, QDialog, QLabel, QLineEdit, QFormLayout, QDialogButtonBox, QComboBox, QMessageBox, \
    QStyleFactory
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from SchoolSystem import SchoolSystem
from GlobalData import global_data

# 假设你已经创建了SchoolSystem的实例school_system
school_system = SchoolSystem('categories.db')


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300,100)
        self.layout = QFormLayout(self)

        self.username = QLineEdit("yedong113")
        self.password = QLineEdit("xinglina113")
        self.password.setEchoMode(QLineEdit.Password)

        self.layout.addRow("Username", self.username)
        self.layout.addRow("Password", self.password)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.login)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)

    def login(self):
        username = self.username.text()
        password = self.password.text()
        user = school_system.validate_user(username, password)
        if user is None:
            QMessageBox.critical(self, "Error", "Invalid username or password.")
        else:
            global_data.username = username
            user_info = school_system.get_user(username)
            global_data.userid = user_info[0]
            stu_list = school_system.get_students(user_info[0])
            for item in stu_list:
                global_data.student_info.append(item)
            self.accept()


# StudentDialog, StudentTable, MainWindow 类的定义与之前相同

import qdarkstyle
def main():
    from simple_point_system import SimplePointSystem
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    from qdarkstyle.light.palette import LightPalette
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    # app.setStyle(QStyleFactory.create("windows"))
    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.Accepted:
        simple_point_system = SimplePointSystem(app)
        simple_point_system.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
