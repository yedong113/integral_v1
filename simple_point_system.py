import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QComboBox, QLineEdit,
                             QPushButton, QWidget, QFormLayout, QDateEdit, QTextEdit, QDialog,
                             QTableView, QAbstractItemView, QMenuBar, QAction, QHeaderView, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate
import datetime
from category_management import CategoryManagement
from month_query import PointsDialog

from PyQt5.QtGui import QStandardItemModel, QStandardItem


class SimplePointSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.menuBar = QMenuBar(self)
        self.initUI()
        self.showMaximized()

    def initUI(self):
        self.setWindowTitle('简易积分系统')
        fileMenu = self.menuBar.addMenu("操作")
        editMenu = self.menuBar.addMenu("设置")
        statMenu = self.menuBar.addMenu("统计分析")
        helpMenu = self.menuBar.addMenu("帮助")
        openAction = QAction("添加积分", self)
        openAction.triggered.connect(self.showSubmitDialog)
        fileMenu.addAction(openAction)
        queryAction = QAction("查询积分", self)
        queryAction.triggered.connect(self.query_points)
        fileMenu.addAction(queryAction)
        refreshAction = QAction("刷新", self)
        refreshAction.triggered.connect(self.query_all_points)
        fileMenu.addAction(queryAction)

        saveAction = QAction("保存", self)
        saveAction.triggered.connect(self.save_file)
        fileMenu.addAction(saveAction)

        typeSetting = QAction("积分类别设置", self)
        typeSetting.triggered.connect(self.type_setting)
        editMenu.addAction(typeSetting)


        statMonthAction = QAction("按月查询", self)
        statMonthAction.triggered.connect(self.stat_month)
        statMenu.addAction(statMonthAction)


        aboutAction = QAction("关于", self)
        aboutAction.triggered.connect(self.show_about_dialog)
        helpMenu.addAction(aboutAction)

        self.initDatabase()

        # 创建日期选择器和查询按钮
        date_label = QLabel("选择日期：")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.query_button = QPushButton("查询积分")
        self.query_button.clicked.connect(self.query_points)
        self.query_all_button = QPushButton("刷新")
        self.query_all_button.clicked.connect(self.query_all_points)

        self.add_button = QPushButton("添加积分")
        self.add_button.clicked.connect(self.showSubmitDialog)

        # 创建一个 QHBoxLayout 实例
        date_layout = QHBoxLayout()
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        date_layout.addWidget(self.query_button)
        date_layout.addWidget(self.query_all_button)
        date_layout.addWidget(self.add_button)
        date_layout.addStretch(1)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setMenuBar(self.menuBar)

        self.points_table = QTableView()
        self.points_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.points_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.loadPoints()

        layout.addLayout(date_layout)
        layout.addWidget(self.points_table)

        central_widget = QWidget()

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def stat_month(self):
        # 在这里实现显示关于对话框的逻辑
        self.points_dialog = PointsDialog()
        self.points_dialog.show()

    def query_points(self):
        # 获取选定的日期
        self.load_by_date()

    def query_all_points(self):
        # 获取选定的日期
        self.load_all_points()

    def initDatabase(self):
        self.conn = sqlite3.connect('categories.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS points (
                                   id INTEGER PRIMARY KEY,
                                   name TEXT NOT NULL,
                                   date TEXT NOT NULL,
                                   category_id INTEGER NOT NULL,
                                   points INTEGER NOT NULL,
                                   remark TEXT,
                                   FOREIGN KEY (category_id) REFERENCES categories(id)
                               )''')

        self.conn.commit()

    def load_by_date(self):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        self.cursor.execute('''select *from (SELECT points.name, points.date, categories.name,
                                      points.points, points.remark
                               FROM points 
                               INNER JOIN categories ON points.category_id = categories.id
                               ORDER BY points.date DESC ) where date=? ''', (selected_date,))
        points = self.cursor.fetchall()
        self.load_points(points)

        pass

    def load_all_points(self):
        self.cursor.execute('''SELECT points.name, points.date, categories.name,
                                      points.points, points.remark
                               FROM points
                               INNER JOIN categories ON points.category_id = categories.id
                               ORDER BY points.date DESC''')
        points = self.cursor.fetchall()

        model = QStandardItemModel(len(points), 5)
        model.setHorizontalHeaderLabels(['姓名', '日期', '积分类别', '积分', '备注'])

        for row, point in enumerate(points):
            for col, value in enumerate(point):
                model.setItem(row, col, QStandardItem(str(value)))

        self.points_table.setModel(model)

    def load_points(self, points):
        model = QStandardItemModel(len(points), 5)
        model.setHorizontalHeaderLabels(['姓名', '日期', '积分类别', '积分', '备注'])

        for row, point in enumerate(points):
            for col, value in enumerate(point):
                model.setItem(row, col, QStandardItem(str(value)))

        self.points_table.setModel(model)

    def loadPoints(self):
        self.cursor.execute('''SELECT points.name, points.date, categories.name,
                                      points.points, points.remark
                               FROM points
                               INNER JOIN categories ON points.category_id = categories.id
                               ORDER BY points.date DESC''')
        points = self.cursor.fetchall()

        model = QStandardItemModel(len(points), 5)
        model.setHorizontalHeaderLabels(['姓名', '日期', '积分类别', '积分', '备注'])

        for row, point in enumerate(points):
            for col, value in enumerate(point):
                model.setItem(row, col, QStandardItem(str(value)))

        self.points_table.setModel(model)

    def showEvent(self, event):
        super().showEvent(event)
        self.resize_columns()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_columns()

    def resize_columns(self):
        # 设置每列的宽度比例
        column_width_ratios = [1, 1, 3, 1, 3]
        total_width = self.points_table.width() - 2
        column_width = 0

        for i, ratio in enumerate(column_width_ratios):
            column_width = int(total_width * ratio / sum(column_width_ratios))
            self.points_table.setColumnWidth(i, column_width)

    def showSubmitDialog(self):
        submit_dialog = QDialog(self)
        submit_dialog.setWindowTitle('添加积分')

        layout = QVBoxLayout(submit_dialog)

        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        name_input = QLineEdit("叶瑜")
        form_layout.addRow('姓名：', name_input)

        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        form_layout.addRow('日期：', date_input)

        category_label = QLabel('请选择积分类别：')
        layout.addWidget(category_label)

        category_combo = QComboBox()
        self.loadCategories(category_combo)
        layout.addWidget(category_combo)

        points_label = QLabel('请输入积分：')
        layout.addWidget(points_label)

        points_input = QLineEdit()
        layout.addWidget(points_input)

        remark_input = QTextEdit()
        form_layout.addRow('备注：', remark_input)

        submit_button = QPushButton('提交积分')
        layout.addWidget(submit_button)

        def submitPoints():
            name = name_input.text()
            date = date_input.date().toString(Qt.ISODate)
            category_id = category_combo.currentData()
            points = points_input.text()
            remark = remark_input.toPlainText()

            # 在此处进行数据验证，例如检查 points 是否为数字
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            self.cursor.execute('''INSERT INTO points (name, date, category_id, points, remark)
                                   VALUES (?, ?, ?, ?, ?)''', (name, date, category_id, points, remark))
            self.conn.commit()

            # 在此处显示成功消息或清除输入框等
            self.loadPoints()
            submit_dialog.accept()

        submit_button.clicked.connect(submitPoints)

        submit_dialog.exec_()

    def loadCategories(self, combo, parent_id=None, level=0):
        categories = self.getCategories(parent_id)
        for category in categories:
            combo.addItem(' ' * 4 * level + category[2], category[0])
            self.loadCategories(combo, category[0], level + 1)

    def getCategories(self, parent_id):
        if parent_id is None:
            self.cursor.execute('SELECT * FROM categories WHERE parent_id IS NULL')
        else:
            self.cursor.execute('SELECT * FROM categories WHERE parent_id=?', (parent_id,))
        return self.cursor.fetchall()

    def open_file(self):
        # 在这里实现打开文件的逻辑
        pass

    def save_file(self):
        # 在这里实现保存文件的逻辑
        pass

    def show_about_dialog(self):
        # 在这里实现显示关于对话框的逻辑
        pass

    def type_setting(self):
        # 在这里实现显示关于对话框的逻辑
        self.category_management = CategoryManagement()
        self.category_management.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    simple_point_system = SimplePointSystem()
    simple_point_system.show()
    sys.exit(app.exec_())
