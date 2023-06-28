import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QWidget, QTableView, QHeaderView, QLabel, \
    QDateEdit, QPushButton, QHBoxLayout, QMessageBox, QAction, QMenuBar
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate


class PointsDialog(QDialog):
    def __init__(self):
        super().__init__()

        # 创建两个 QDateEdit 实例，分别表示开始和结束月份
        date_label = QLabel("选择月份范围：")
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.start_date_edit.setDisplayFormat("yyyy-MM")
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setDisplayFormat("yyyy-MM")

        # 创建查询按钮
        self.query_button = QPushButton("查询积分")
        self.query_button.clicked.connect(self.query_monthly_points)

        # 创建一个 QHBoxLayout 实例
        date_layout = QHBoxLayout()
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(QLabel("至"))
        date_layout.addWidget(self.end_date_edit)
        date_layout.addStretch(1)
        date_layout.addWidget(self.query_button)

        # 创建一个 QVBoxLayout 实例
        layout = QVBoxLayout()

        # 创建一个 QTableView 实例
        self.table_view = QTableView()

        # 将 QHBoxLayout 和 QTableView 添加到布局中
        layout.addLayout(date_layout)
        layout.addWidget(self.table_view)

        # 设置布局
        self.setLayout(layout)

    def query_monthly_points(self):
        # 获取选定的月份范围
        start_month = self.start_date_edit.date().toString("yyyy-MM")
        end_month = self.end_date_edit.date().toString("yyyy-MM")

        # 连接到数据库
        conn = sqlite3.connect("categories.db")
        cur = conn.cursor()

        # 查询指定月份范围的积分数据
        query = f"select name,SUBSTR(date,0,8) month,SUM(points) points from points WHERE date >= '{start_month}-01' AND date <= '{end_month}-31' group by name,SUBSTR(date,0,8)"
        # query = f"SELECT name, SUM(points) FROM points WHERE date >= '{start_month}-01' AND date <= '{end_month}-31' GROUP BY name"
        cur.execute(query)
        data = cur.fetchall()

        # 关闭数据库连接
        conn.close()

        # 创建并设置模型
        model = QStandardItemModel(len(data), 3)
        model.setHorizontalHeaderLabels(['姓名', '月份', '积分'])

        # 将数据添加到模型
        for row, items in enumerate(data):
            for column, item in enumerate(items):
                model.setItem(row, column, QStandardItem(str(item)))

        # 设置表格视图的模型
        self.table_view.setModel(model)

        # 设置水平表头的调整模式
        horizontal_header = self.table_view.horizontalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.Stretch)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个菜单栏
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # 创建一个菜单项
        points_action = QAction("查询积分", self)
        points_action.triggered.connect(self.show_points_dialog)

        # 将菜单项添加到菜单栏
        menu_bar.addAction(points_action)

    def show_points_dialog(self):
        points_dialog = PointsDialog()
        points_dialog.setWindowTitle("查询积分")
        points_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
