import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QComboBox, QLineEdit, QStyleFactory,
                             QPushButton, QWidget, QFormLayout, QDateEdit, QTextEdit, QDialog, QTreeView, QToolBar,
                             QTableView, QAbstractItemView, QMenuBar, QAction, QHeaderView, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFile, QTextStream
import datetime
from category_management import CategoryManagement
from student_main_window import StudentListDialog
from month_query import PointsDialog

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from point_detail import PointsDetail
from global_data import global_data
from categories import Categories
import qdarkstyle

points_detail = PointsDetail("categories.db")
c_categories = Categories("categories.db")


class SimplePointSystem(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.menuBar = QMenuBar(self)
        self.initUI()
        self.showMaximized()

    def initUI(self):
        self.setWindowTitle('简易积分系统')
        fileMenu = self.menuBar.addMenu("操作")
        editMenu = self.menuBar.addMenu("设置")
        statMenu = self.menuBar.addMenu("统计分析")
        displayStyleMenu = self.menuBar.addMenu("显示风格")
        helpMenu = self.menuBar.addMenu("帮助")
        openIconSmall = QIcon('./img/新增_16.png')
        openAction = QAction(openIconSmall, "添加积分", self)
        openAction.triggered.connect(self.showSubmitDialog)

        fileMenu.addAction(openAction)

        queryIconSmall = QIcon('./img/查询_16.png')
        queryAction = QAction(queryIconSmall, "查询积分", self)
        queryAction.triggered.connect(self.query_points)
        fileMenu.addAction(queryAction)

        refreshIcon = QIcon('./img/刷新.png')
        refreshAction = QAction(refreshIcon, "刷新", self)
        refreshAction.triggered.connect(self.query_all_points)
        fileMenu.addAction(refreshAction)

        saveAction = QAction("保存", self)
        saveAction.triggered.connect(self.save_file)
        fileMenu.addAction(saveAction)

        studentSettingIcon = QIcon('./img/学生信息设置.png')
        studentSetting = QAction(studentSettingIcon, "学生信息设置", self)
        studentSetting.triggered.connect(self.student_setting)
        editMenu.addAction(studentSetting)

        typeIcon = QIcon('./img/类别设置.png')
        typeSetting = QAction(typeIcon, "积分类别设置", self)
        typeSetting.triggered.connect(self.type_setting)
        editMenu.addAction(typeSetting)

        statMonthIcon = QIcon('./img/统计.png')
        statMonthAction = QAction(statMonthIcon, "按月查询", self)
        statMonthAction.triggered.connect(self.stat_month)
        statMenu.addAction(statMonthAction)

        # displayStyleAction = QAction("windows", self)
        # displayStyleAction.triggered.connect(self.windows_style)
        # displayStyleMenu.addAction(displayStyleAction)

        # Ubuntu ElegantDark  MaterialDark  ConsoleStyle AMOLED Aqua MacOS.qss
        UbuntuStyleAction = QAction("Ubuntu", self)
        UbuntuStyleAction.triggered.connect(self.Ubuntu_style)
        displayStyleMenu.addAction(UbuntuStyleAction)

        displayElegantDarkAction = QAction("ElegantDark", self)
        displayElegantDarkAction.triggered.connect(self.ElegantDark_style)
        displayStyleMenu.addAction(displayElegantDarkAction)

        displayElegantLightAction = QAction("ElegantLight", self)
        displayElegantLightAction.triggered.connect(self.ElegantLight_style)
        displayStyleMenu.addAction(displayElegantLightAction)


        displayMacAction = QAction("MacOS", self)
        displayMacAction.triggered.connect(self.mac_style)
        displayStyleMenu.addAction(displayMacAction)

        aboutIcon = QIcon('./img/关于.png')
        aboutAction = QAction(aboutIcon, "关于", self)
        aboutAction.triggered.connect(self.show_about_dialog)
        helpMenu.addAction(aboutAction)

        self.toolbar = QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(queryAction)
        self.toolbar.addAction(refreshAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(studentSetting)
        self.toolbar.addAction(typeSetting)
        self.toolbar.addSeparator()
        self.toolbar.addAction(statMonthAction)
        self.addToolBar(self.toolbar)

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
        layout.addWidget(self.toolbar)

        self.points_table = QTableView()
        self.points_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.points_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.loadPoints()

        layout.addLayout(date_layout)
        layout.addWidget(self.points_table)

        central_widget = QWidget()

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_style(self,file_name):
        file = QFile(file_name)
        if file.open(QFile.ReadOnly | QFile.Text):
            # 使用QTextStream读取QSS文件内容
            stream = QTextStream(file)
            style_sheet = stream.readAll()

            # 设置应用程序的样式表
            self.app.setStyleSheet(style_sheet)

    def Ubuntu_style(self):
        self.load_style("./QSS-master/Ubuntu.qss")

    def ElegantDark_style(self):
        # self.load_style("./QSS-master/ElegantDark.qss")
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    def ElegantLight_style(self):
        # self.load_style("./QSS-master/ElegantDark.qss")
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        from qdarkstyle.light.palette import LightPalette
        self.app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5',palette=LightPalette))

    # fusion_style ElegantLight_style
    def fusion_style(self):
        self.app.setStyle(QStyleFactory.create("Fusion"))

    def mac_style(self):
        self.load_style("./QSS-master/MacOS.qss")

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
        pass

    def load_by_date(self):
        # 按登录用户名和日期获取积分记录
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        points = points_detail.list_by_date_and_user_id(selected_date, global_data.username)
        self.load_points(points)
        pass

    def load_all_points(self):
        points = points_detail.list_by_user_id(global_data.username)
        self.load_points(points)

    def load_points(self, points):
        model = QStandardItemModel(len(points), 5)
        model.setHorizontalHeaderLabels(['姓名', '日期', '积分类别', '积分', '备注'])

        for row, point in enumerate(points):
            for col, value in enumerate(point):
                if value is not None:
                    model.setItem(row, col, QStandardItem(str(value)))
                else:
                    model.setItem(row, col, QStandardItem(str('')))

        self.points_table.setModel(model)

    def loadPoints(self):
        points = points_detail.list_by_user_id(global_data.username)
        self.load_points(points)

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
        submit_dialog.resize(800, 600)
        submit_dialog.setWindowTitle('添加积分')

        layout = QVBoxLayout(submit_dialog)

        form_layout = QFormLayout()
        layout.addLayout(form_layout)
        name_combo = QComboBox()
        form_layout.addRow('姓名：', name_combo)
        for item in global_data.student_info:
            name_combo.addItem(item[1], item[0])

        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        form_layout.addRow('日期：', date_input)

        category_label = QLabel('请选择积分类别：')
        # layout.addWidget(category_label)

        category_tree = QTreeView()
        # category_tree.setStyleSheet("""
        #     QTreeView::branch:has-children:!has-siblings:closed,
        #     QTreeView::branch:closed:has-children:has-siblings {
        #             border-image: none;
        #             image: url(branch-closed.png);
        #     }
        #     QTreeView::branch:open:has-children:!has-siblings,
        #     QTreeView::branch:open:has-children:has-siblings  {
        #             border-image: none;
        #             image: url(branch-open.png);
        #     }
        #     QTreeView::branch:has-siblings:!adjoins-item {
        #         border-image: url(vline.png) 0;
        #     }
        #     QTreeView::branch:has-siblings:adjoins-item {
        #         border-image: url(branch-more.png) 0;
        #     }
        #     QTreeView::branch:!has-children:!has-siblings:adjoins-item {
        #         border-image: url(branch-end.png) 0;
        #     }
        # """)
        self.loadCategoriesTree(category_tree)
        form_layout.addRow('请选择积分类别：', category_tree)
        # form_layout.addWidget(category_tree)
        # layout.addWidget(category_tree)

        points_input = QLineEdit()
        form_layout.addRow('请输入积分：', points_input)

        remark_input = QTextEdit()
        form_layout.addRow('备注：', remark_input)

        submit_button = QPushButton('提交积分')
        layout.addWidget(submit_button)

        def submitPoints():
            select_index = name_combo.currentIndex()
            stu_id = name_combo.itemData(select_index)
            date = date_input.date().toString(Qt.ISODate)
            indexes = category_tree.selectionModel().selectedIndexes()
            category_id = indexes[0].data()
            # category_id = category_tree.sel
            points = points_input.text()
            remark = remark_input.toPlainText()

            points_detail.create(student_id=stu_id, date=date, category_id=category_id, points=points,
                                 user_id=global_data.username)
            self.loadPoints()
            submit_dialog.accept()

        submit_button.clicked.connect(submitPoints)

        submit_dialog.exec_()

    def loadCategoriesTree(self, category_tree):
        categories = c_categories.list_all()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['id', 'name'])
        rootItem = model.invisibleRootItem()
        parent_dict = {}

        for id, parent_id, name, points in categories:
            parent = parent_dict.get(parent_id, rootItem)
            item = QStandardItem(str(id))
            item3 = QStandardItem(name)
            parent.appendRow([item, item3])
            parent_dict[id] = item

        category_tree.setModel(model)

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

    def student_setting(self):
        self.student_dialog = StudentListDialog()
        self.student_dialog.show()
