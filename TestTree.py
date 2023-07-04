from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QVBoxLayout, QMenuBar, QWidget, QMenu
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 创建菜单栏并添加到布局中
        menubar = QMenuBar()
        fileIcon = QIcon('./img/操作.png')  # 使用你的图标文件的路径
        fileMenu = QMenu('File', self)
        fileMenu.setIcon(fileIcon)
        menubar.addMenu(fileMenu)
        layout.addWidget(menubar)

        # 创建工具栏并添加到布局中
        toolbar = QToolBar()
        fileAction = QAction(fileIcon, 'File', self)
        toolbar.addAction(fileAction)
        layout.addWidget(toolbar)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
