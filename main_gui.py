# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import *

# app = QApplication([])
# main_win = QWidget()

# def button_func():
#     print("button pressed")

# #modify screen
# main_win.setWindowTitle("Casino GUI")
# main_win.resize(1000,1000)
# main_win.move(200,0)


# #create button
# button_next = QPushButton('Generate')
# button_next.setText("NEXT")
# button_next.text()
# button_next.clicked.connect(button_func)

# #label


# line = QVBoxLayout()
# line.addWidget(button_next, alignment= Qt.AlignCenter)
# main_win.setLayout(line)


# main_win.show()
# app.exec_()


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel)
from PyQt5.QtGui import QIcon

from TomScreen import PlinkoGame
# from Vinhscreen import RouletteWheel


class FirstScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Health Check")
        self.resize(800, 500)
        self.create_widget()
        self.show()
        self.next_screen()
    
    def create_widget(self):
        title1 = QLabel("Welcome to Casino game!")

        self.button_Plinko = QPushButton("", self)
        self.button_Plinko.setStyleSheet("background-image: url(Images/Plinko.png); border: none;") 
        self.button_Plinko.setFixedSize(250, 200)
        self.button_Plinko.clicked.connect(self.ScreenPlinko) 
        
        

        self.button_Roulette = QPushButton("")
        self.button_Roulette.setStyleSheet("background-image: url(Images/Roulette.png); border: none;") 
        self.button_Roulette.setFixedSize(250, 200)
        self.button_Plinko.clicked.connect(self.ScreenPlinko) 

        #Create layout
        line1 = QHBoxLayout()
        line2 = QHBoxLayout()
        line3 = QHBoxLayout()
        main_line = QVBoxLayout()
        line1.addWidget(title1, alignment=Qt.AlignCenter)
        line3.addWidget(self.button_Plinko, alignment=Qt.AlignCenter)
        line3.addWidget(self.button_Roulette, alignment=Qt.AlignCenter)
        main_line.addLayout(line1)
        main_line.addLayout(line2)
        main_line.addLayout(line3)
        self.setLayout(main_line)
        
    def ScreenPlinko(self):
        # print("start click")
        self.ScreenPlinko = PlinkoGame()
        self.ScreenPlinko.show()
        self.hide()
        
    def next_screen(self):     
        self.button_Plinko.clicked.connect(self.ScreenPlinko) 
                
# Run application
app = QApplication([])

#Show and run the application
main_win = FirstScreen()
app.exec_()

