import sys
from main_windows import LoginWindow
from PyQt5.QtWidgets import QApplication
import numpy as np

"""
dokumentacja tego syfu
https://doc.qt.io/qtforpython/api.html
help https://python-catalin.blogspot.com/2018/11/python-qt5-setstylesheet-example.html
rgb creator https://www.rapidtables.com/web/color/RGB_Color.html
https://docs.python.org/2/library/sqlite3.html
https://python101.readthedocs.io/pl/latest/pyqt/index.html
"""
pos = np.array([0, 0])
width = 1000
height = 600
text_height = 20
middle_of_screen = np.array([1920/2 - width/2, 1080/2 - height/2])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Window\'s closing')
