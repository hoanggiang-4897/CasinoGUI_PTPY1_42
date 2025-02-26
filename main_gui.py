from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

app = QApplication([])
main_win = QWidget()

def button_func():
    print("button pressed")

#modify screen
main_win.setWindowTitle("Casino GUI")
main_win.resize(1000,1000)
main_win.move(200,0)


#create button
button_next = QPushButton('Generate')
button_next.setText("NEXT")
button_next.text()
button_next.clicked.connect(button_func)

#label


line = QVBoxLayout()
line.addWidget(button_next, alignment= Qt.AlignCenter)
main_win.setLayout(line)


main_win.show()
app.exec_()


