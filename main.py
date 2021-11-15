import sys
from window import Window
from PyQt5.QtWidgets import QApplication
import numpy as np

"""
dokumentacja tego syfu
https://doc.qt.io/qtforpython/api.html
help https://python-catalin.blogspot.com/2018/11/python-qt5-setstylesheet-example.html
rgb creator https://www.rapidtables.com/web/color/RGB_Color.html
"""
pos = np.array([0, 0])
width = 1000
heigth = 600
text_heigth = 20
middle_of_screen = np.array([1920/2 - width/2, 1080/2 - heigth/2])

def login_screen():
    global pos, middle_of_screen, text_heigth, width, heigth
    window = Window()
    window.setup(middle_of_screen + pos, width=width, heigth=heigth, title="Login Screen")
    window.add_label("text", [50, 50], [50, text_heigth])
    window.add_button("Zaloguj", [width/2 - 50, heigth/2 - 10])
    window.show()
    pos += 50


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # login_screen()
    window_1 = Window()
    window_1.setup(middle_of_screen + pos, width=width, heigth=heigth, title="Login Screen")
    window_1.add_label("text", [50, 50], [50, text_heigth], (148, 165, 247))
    window_1.add_button("Zaloguj", [width/2 - 50, heigth/2 - 10], (255, 0, 0))
    window_1.add_line_edit("line edit", [100, 100], (94, 239, 118))
    window_1.add_button("Click me", [100, 200], (94, 239, 118))
    window_1.show()
    pos += 50

# window_2 = Window()
# window_2.setup(middle_of_screen + pos, width=width, heigth=heigth, title="autobus")
# window_2.show()

    sys.exit(app.exec_())
