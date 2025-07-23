import sys
import math
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class RouletteGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roulette")
        self.setGeometry(300, 100, 1200, 700)
        self.setStyleSheet("background-color: #38726C;")
        self.balance = 1000
        self.result = {"winning_slot": None, "player_slot": None, "bet_amount": 0}

        self.init_ui()

    def init_ui(self):
        layout1 = QVBoxLayout()

        title = QLabel("Roulette")
        title.setFont(QFont("Arial", 100))
        title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        title.setStyleSheet("color: #FAFAFF;")
        layout1.addWidget(title)

        tutorial = QLabel("Roulette is a casino game where players bet on where a ball will land on a spinning wheel.")
        tutorial.setFont(QFont("Arial", 20))
        tutorial.setAlignment(Qt.AlignLeft)
        tutorial.setStyleSheet("color: #FAFAFF;")
        layout1.addWidget(tutorial)

        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QHBoxLayout()

        self.betting = QLineEdit("Your bet (must be a positive integer)")
        self.betting.setFixedSize(300, 75)
        self.betting.setAlignment(Qt.AlignCenter)
        self.betting.setStyleSheet("""
            QLineEdit {
                background-color: #FAFAFF;
                color: #0D0A0B;
                font-size: 16px;
                border: 2px solid #72B01D;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        layout4.addWidget(self.betting)

        self.slot_input = QLineEdit("Your slot (1 - 36)")
        self.slot_input.setFixedSize(300, 75)
        self.slot_input.setAlignment(Qt.AlignCenter)
        self.slot_input.setStyleSheet("""
            QLineEdit {
                background-color: #FAFAFF;
                color: #0D0A0B;
                font-size: 16px;
                border: 2px solid #72B01D;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        layout4.addWidget(self.slot_input)

        self.balance_display = QLabel(f"Balance: ${self.balance}")
        self.balance_display.setFixedSize(600, 75)
        balance_font = QFont("Arial", 24)
        balance_font.setBold(True)
        self.balance_display.setFont(balance_font)
        self.balance_display.setAlignment(Qt.AlignHCenter)
        self.balance_display.setStyleSheet("color: #E03616;")
        layout3.addWidget(self.balance_display)
        layout3.addLayout(layout4, Qt.AlignTop)

        self.confirm_btn = QPushButton("Confirm your bet and slot")
        self.confirm_btn.setFixedSize(600, 75)
        self.confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #E03616;
                color: #FAFAFF;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #72B01D;
                color: #0D0A0B;
            }
        """)
        self.confirm_btn.clicked.connect(self.process_bet)
        layout3.addWidget(self.confirm_btn)

        self.confirm_txt = QLabel("Everything you confirmed will be here")
        self.confirm_txt.setFixedSize(600, 75)
        self.confirm_txt.setFont(QFont("Arial", 20))
        self.confirm_txt.setAlignment(Qt.AlignCenter)
        self.confirm_txt.setStyleSheet("color: #FAFAFF;")
        layout3.addWidget(self.confirm_txt)

        layout3_widget = QWidget()
        layout3_widget.setLayout(layout3)
        layout3_widget.setFixedWidth(600)

        self.wheel = self.RouletteWheel(self)

        wheel_container = QVBoxLayout()
        wheel_container.addWidget(self.wheel, alignment=Qt.AlignCenter)

        layout2.addWidget(layout3_widget, alignment=Qt.AlignLeft)
        layout2.addLayout(wheel_container)
        layout1.addLayout(layout2)

<<<<<<< HEAD
        #main screen button
        self.button_mainScreen = QPushButton("Back to main screen")
        layout1.addWidget(self.button_mainScreen)

=======
>>>>>>> 0afe9672b24c5a7969dec88680a6cbf96263cf32
        self.setLayout(layout1)

    def process_bet(self):
        bet_text = self.betting.text()
        slot_text = self.slot_input.text()
        slot_list = [str(i + 1) for i in range(36)]

        if bet_text.isdigit() and slot_text in slot_list:
            bet = int(bet_text)
            if bet > self.balance or bet <= 0:
                self.confirm_txt.setText("Insufficient balance or invalid bet.")
            else:
                self.result["bet_amount"] = bet
                self.result["player_slot"] = int(slot_text)
                self.result["winning_slot"] = random.randint(1, 36)
                self.confirm_txt.setText(f"${bet} on slot {slot_text}. Spinning...")
                self.wheel.start_spin(self.result["winning_slot"])
        else:
            self.confirm_txt.setText("Invalid input.")

        self.betting.setText("Your bet (must be a positive integer)")
        self.slot_input.setText("Your slot (1 - 36)")

    def show_result(self):
        if self.result["player_slot"] == self.result["winning_slot"]:
            win = self.result["bet_amount"] * 36
            self.balance += win
            self.confirm_txt.setText(f"🎉 You WON! Slot {self.result['winning_slot']}. You earned ${win}")
        else:
            self.balance -= self.result["bet_amount"]
            self.confirm_txt.setText(f"❌ You lost. Winning slot: {self.result['winning_slot']}")
        self.balance_display.setText(f"Balance: ${self.balance}")

    class RouletteWheel(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.setFixedSize(500, 500)
            self.highlight_slot = None
            self.winning_slot = None

            # Timer for moving highlight
            self.timer = QTimer()
            self.timer.timeout.connect(self.advance_highlight)

            self.current_index = 0
            self.steps_remaining = 0
            self.total_steps = 0

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            center = self.rect().center()
            radius = self.rect().width() // 2

            painter.setBrush(QBrush(Qt.black))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.rect())

            angle_step = 360 / 36
            font = QFont("Arial", 10)
            painter.setFont(font)

            for i in range(36):
                if self.highlight_slot == i + 1:
                    color = QColor("yellow")
                    text_color = QColor("black")
                else:
                    color = QColor("red") if i % 2 == 0 else QColor("black")
                    text_color = QColor("white")
                painter.setBrush(QBrush(color))
                start_angle = int(i * angle_step * 16)
                span_angle = int(angle_step * 16)
                painter.drawPie(self.rect(), start_angle, span_angle)

                angle_deg = i * angle_step + angle_step / 2
                cx = center.x() + (radius - 30) * math.cos(math.radians(angle_deg))
                cy = center.y() - (radius - 30) * math.sin(math.radians(angle_deg))
                painter.setPen(text_color)
                painter.drawText(QRectF(cx - 12, cy - 12, 24, 24), Qt.AlignCenter, str(i + 1))

            painter.setBrush(QBrush(QColor("#72B01D")))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.rect().adjusted(100, 100, -100, -100))

        def start_spin(self, winning_slot):
            self.winning_slot = winning_slot
            self.current_index = 0
            self.steps_remaining = random.randint(36, 72)  # Random full spins
            self.total_steps = self.steps_remaining
            self.timer.start(40)

        def advance_highlight(self):
            self.current_index = (self.current_index + 1) % 36
            self.highlight_slot = self.current_index + 1
            self.steps_remaining -= 1
            self.update()

            if self.steps_remaining <= 0 and self.highlight_slot == self.winning_slot:
                self.timer.stop()
                self.parent.show_result()


# --- Run the Game ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RouletteGame()
    game.show()
<<<<<<< HEAD
    sys.exit(app.exec_())
=======
    sys.exit(app.exec_())
>>>>>>> 0afe9672b24c5a7969dec88680a6cbf96263cf32
