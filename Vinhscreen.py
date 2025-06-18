import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#App
app = QApplication(sys.argv)

#Widget(main window)
window = QWidget()
window.setWindowTitle("Roulette")
window.setGeometry(300, 300, 1200, 700)

###Layout###
#Layout 1
layout1 = QVBoxLayout()
title = QLabel("Roulette")
title_font = QFont("Arial", 100)
title.setFont(title_font)
title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
layout1.addWidget(title)
tutorial = QLabel("Roulette is a casino game where players bet on where a ball will land on a spinning wheel.")
tutorial_font = QFont("Arial", 20)
tutorial.setAlignment(Qt.AlignLeft)
tutorial.setFont(tutorial_font)
layout1.addWidget(tutorial)

###LAYOUTS###
layout2 = QHBoxLayout()
layout3 = QVBoxLayout()
layout4 = QHBoxLayout()

###LAYOUT 4###
#Betting input
betting = QLineEdit("Your bet (must be a positive integer)")
betting.setFixedSize(300, 75)
betting.setAlignment(Qt.AlignCenter)
layout4.addWidget(betting)
#Slot input
slot = QLineEdit("Your slot (1 - 36)")
slot.setFixedSize(300, 75)
slot.setAlignment(Qt.AlignCenter)
layout4.addWidget(slot, alignment = Qt.AlignLeft)

###LAYOUT 3###
#Balance label
balance = 1000
bl_text = f"Balance: ${str(balance)}"
balance_display = QLabel(bl_text)
balance_display.setFixedSize(600, 75)
layout3.addWidget(balance_display)

def balance_func(bl:int, bet:int, label = QLabel()) -> int: 
    bl -= bet
    text = f"Balance: ${str(bl)}"
    label.setText(text)

layout3.addLayout(layout4, Qt.AlignTop)
#Confirm button
confirm_btn = QPushButton()
confirm_btn.setFixedSize(600, 75)
confirm_btn.setText("Confirm your bet and slot")
layout3.addWidget(confirm_btn)
#Confirm text
confirm_txt = QLabel()
confirm_txt.setText("Everything you confirmed will be here")
confirm_txt.setFixedSize(600, 75)
confirm_txt.setAlignment(Qt.AlignCenter)

slot_list = []
for i in range(36):
    slot_list.append(str(i + 1))
def show(bl:int, bl_display = QLabel(), bet = QLineEdit(), slot = QLineEdit(), list = list, label = QLabel()):
    current_bet =  bet.text()
    current_slot = slot.text()
    if current_bet.isdigit() == True and current_slot in list:
        text = f"${current_bet} on slot {current_slot}"
        label.setText(text)
        balance_func(bl, int(current_bet), bl_display)
    else:
        label.setText("Invalid input.")
    bet.setText("Your bet (must be a positive integer)")
    slot.setText("Your slot (1 - 36)")
confirm_btn.clicked.connect(lambda: show(balance, balance_display, betting, slot, slot_list, confirm_txt))
layout3.addWidget(confirm_txt)
#Set fixed width for layout 3
layout3_widget = QWidget()
layout3_widget.setLayout(layout3)
layout3_widget.setFixedWidth(600)

layout2.addWidget(layout3_widget, alignment = Qt.AlignLeft)
layout1.addLayout(layout2)


#Show the window
window.setLayout(layout1)
window.show()

#Run the app's event loop
sys.exit(app.exec_())