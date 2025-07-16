import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel)
from PyQt5.QtGui import QIcon

from TomScreen import PlinkoGame
from Vinhscreen import RouletteGame


class FirstScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Casino Game")
        self.resize(800, 500)
        self.create_widget()
        self.show()
    
    def create_widget(self):
        title1 = QLabel("Welcome to Casino game!")

        self.button_Plinko = QPushButton("", self)
        self.button_Plinko.setStyleSheet("background-image: url(Images/Plinko.png); border: none;") 
        self.button_Plinko.setFixedSize(250, 200)
        self.button_Plinko.clicked.connect(self.Switch_Plinko_Screen) 
        
        self.button_Roulette = QPushButton("")
        self.button_Roulette.setStyleSheet("background-image: url(Images/Roulette.png); border: none;") 
        self.button_Roulette.setFixedSize(250, 200)
        self.button_Roulette.clicked.connect(self.Switch_Roulette_Screen) 

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
                
    def Switch_Plinko_Screen(self):
        # print("start click")
        self.ScreenPlinko = PlinkoGame()
        self.ScreenPlinko.show()
        self.hide()

    def Switch_Roulette_Screen(self):
        # print("start click")
        self.RouletteScreen = RouletteGame()
        self.RouletteScreen.show()
        self.hide()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = FirstScreen()
    sys.exit(app.exec_())