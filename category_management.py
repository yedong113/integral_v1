import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QWidget,
                             QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt


class CategoryManagement(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('积分类别管理')

        self.initDatabase()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabels(['积分类别'])
        self.category_tree.itemSelectionChanged.connect(self.onCategorySelected)

        self.loadCategories()
        layout.addWidget(self.category_tree)

        add_category_layout = QHBoxLayout()
        layout.addLayout(add_category_layout)

        form_layout = QFormLayout()
        add_category_layout.addLayout(form_layout)

        self.parent_id_label = QLabel()
        form_layout.addRow('上级分类ID', self.parent_id_label)
        self.parent_id_edit_label = QLabel()
        form_layout.addRow('', self.parent_id_edit_label)

        self.category_name_input = QLineEdit()
        form_layout.addRow('分类名称', self.category_name_input)

        add_button = QPushButton('添加分类')
        add_category_layout.addWidget(add_button)
        add_button.clicked.connect(self.addCategory)
        # 添加修改按钮
        modify_button = QPushButton('修改分类')
        add_category_layout.addWidget(modify_button)
        modify_button.clicked.connect(self.modifyCategory)

    def initDatabase(self):
        self.conn = sqlite3.connect('categories.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   parent_id INTEGER,
                                   name TEXT NOT NULL,
                                   FOREIGN KEY (parent_id) REFERENCES categories (id)
                               )''')
        self.conn.commit()

    def onCategorySelected(self):
        selected_item = self.category_tree.currentItem()
        if selected_item:#self.parent_id_edit_label
            parent_id_edit = selected_item.data(0,Qt.UserRole)
            self.parent_id_edit_label.setText(str(parent_id_edit))
            category_name = selected_item.text(0)
            self.category_name_input.setText(category_name)
        else:
            self.category_name_input.clear()

    def loadCategories(self):
        self.category_tree.clear()
        self.addCategoriesToTree(None, None)

    def addCategoriesToTree(self, parent_id, parent_item):
        categories = self.getCategories(parent_id)
        for category in categories:
            item = QTreeWidgetItem()
            item.setText(0, str(category[2]))
            item.setData(0, Qt.UserRole, category[0])

            if parent_item is None:
                self.category_tree.addTopLevelItem(item)
            else:
                parent_item.addChild(item)

            self.addCategoriesToTree(category[0], item)

    def modifyCategory(self):
        selected_item = self.category_tree.currentItem()
        if not selected_item:
            QMessageBox.warning(self, '警告', '请先选择一个分类！')
            return

        category_name = self.category_name_input.text().strip()
        if not category_name:
            QMessageBox.warning(self, '警告', '分类名称不能为空！')
            return

        category_id = selected_item.data(0, Qt.UserRole)
        self.cursor.execute('UPDATE categories SET name = ? WHERE id = ?', (category_name, category_id))
        self.conn.commit()

        self.loadCategories()

    def getCategories(self, parent_id):
        if parent_id is None:
            self.cursor.execute('SELECT * FROM categories WHERE parent_id IS NULL')
        else:
            self.cursor.execute('SELECT * FROM categories WHERE parent_id=?', (parent_id,))
        return self.cursor.fetchall()

    def addCategory(self):
        parent_item = self.category_tree.currentItem()
        if parent_item is not None:
            parent_id = parent_item.data(0, Qt.UserRole)
            self.parent_id_label.setText(str(parent_id))
        else:
            parent_id = None
            self.parent_id_label.setText("无")

        category_name = self.category_name_input.text().strip()
        if not category_name:
            QMessageBox.warning(self, '警告', '分类名称不能为空！')
            return

        self.cursor.execute('INSERT INTO categories (parent_id, name) VALUES (?, ?)',
                            (parent_id, category_name))
        self.conn.commit()

        self.loadCategories()


"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    category_management = CategoryManagement()
    category_management.show()
    sys.exit(app.exec_())
"""
