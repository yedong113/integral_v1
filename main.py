import os
import sys

from PyQt5.QtWidgets import QApplication

def main():
    from simple_point_system import SimplePointSystem
    app = QApplication(sys.argv)
    simple_point_system = SimplePointSystem()
    simple_point_system.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()