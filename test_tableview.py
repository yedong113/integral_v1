from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableView, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个 QTableView 实例
        self.table_view = QTableView()

        # 为 QTableView 设置模型
        model = QStandardItemModel(5, 3)
        model.setHorizontalHeaderLabels(['姓名', '年龄', '职业'])
        self.table_view.setModel(model)

        # 添加数据到模型
        data = [
            ('张三', '25', '程序员'),
            ('李四', '30', '设计师'),
            ('王五', '28', '产品经理'),
            ('赵六', '22', '实习生'),
            ('陈七', '35', '项目经理项目经理项目经理项目经理项目经理项目经理')
        ]

        for row, items in enumerate(data):
            for column, item in enumerate(items):
                model.setItem(row, column, QStandardItem(item))

        # 设置水平表头的调整模式
        # horizontal_header = self.table_view.horizontalHeader()
        # horizontal_header.setSectionResizeMode(QHeaderView.Stretch)

        # 创建一个 QVBoxLayout 实例
        layout = QVBoxLayout()

        # 将 QTableView 添加到布局中
        layout.addWidget(self.table_view)

        # 将布局设置为主窗口的中心部件
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 初始化列宽
        self.resize_columns()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_columns()

    def resize_columns(self):
        # 设置每列的宽度比例
        column_width_ratios = [2, 1, 2]
        total_width = self.table_view.width() - 2  # 减去边框宽度
        self.table_view.setColumnWidth(0, int(total_width/5*2))
        self.table_view.setColumnWidth(1, int(total_width/5))
        self.table_view.setColumnWidth(2, int(total_width/5*2))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
