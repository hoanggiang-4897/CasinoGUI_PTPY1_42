import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget,
        QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QStackedWidget,QMainWindow)

from PyQt5.QtGui import *
from TomScreen import PlinkoGame
from Vinhscreen import RouletteGame


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.create_widget()
        

        
    def create_widget(self):
        
        title1 = QLabel("Welcome to Casino game!")
        title1.setFont(QFont('Times', 50))

        self.button_Plinko = QPushButton("", self)
        self.button_Plinko.setStyleSheet("background-image: url(Images/Plinko.png); border: none;") 
        self.button_Plinko.setFixedSize(250, 200)
        # self.button_Plinko.clicked.connect(self.Switch_Plinko_Screen) 
        
        self.button_Roulette = QPushButton("")
        self.button_Roulette.setStyleSheet("background-image: url(Images/Roulette.png); border: none;") 
        self.button_Roulette.setFixedSize(250, 200)
        # self.button_Roulette.clicked.connect(self.Switch_Roulette_Screen) 

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

        exit_lable = QLabel("Press ESC to exit")
        exit_lable.setAlignment(Qt.AlignCenter)
        main_line.addWidget(exit_lable)
        self.setLayout(main_line)


    


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Casino Game")
        self.resize(500, 500)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.setGeometry(100, 100, 600, 400)

        self.Main_Screen = MainScreen()

        self.screen1 = PlinkoGame()
        self.screen2 = RouletteGame()

        self.stacked_widget.addWidget(self.Main_Screen)
        self.stacked_widget.addWidget(self.screen1)
        self.stacked_widget.addWidget(self.screen2)

        self.Main_Screen.button_Plinko.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.screen1))
        self.Main_Screen.button_Roulette.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.screen2))
        self.screen1.button_mainScreen.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Main_Screen))
        self.screen2.button_mainScreen.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.Main_Screen))

    def keyPressEvent(self, event):
        # Exit full screen on Escape key press
        if event.key() == Qt.Key_Escape:
            self.close()   

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    # window.show()
    window.showFullScreen()
    app.exec_()