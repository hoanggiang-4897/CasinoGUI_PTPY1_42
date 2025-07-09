import sys
import math
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --- Main Window Setup ---
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Roulette")
window.setGeometry(300, 100, 1200, 700)
window.setStyleSheet("background-color: #72B01D;")  # Light green BG from palette

# --- Global game state ---
balance = 1000

# --- Roulette Wheel Widget ---
class RouletteWheel(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 500)
        self.rotation_angle = 0
        self.target_angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.spin_speed = 20
        self.spins_remaining = 0
        self.winning_slot = None
        self.highlight_slot = None
        self.highlight_timer = QTimer()
        self.highlight_timer.setSingleShot(True)
        self.highlight_timer.timeout.connect(self.clear_highlight)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = self.rect().center()
        radius = self.rect().width() // 2

        painter.translate(center)
        painter.rotate(self.rotation_angle)
        painter.translate(-center)

        painter.setBrush(QBrush(Qt.black))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect())

        angle_step = 360 / 36
        font = QFont("Arial", 10)
        painter.setFont(font)

        for i in range(36):
            # Highlight the winning slot yellow
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
            text = str(i + 1)
            text_rect = QRectF(cx - 12, cy - 12, 24, 24)
            painter.drawText(text_rect, Qt.AlignCenter, text)

        painter.setBrush(QBrush(QColor("#38726C")))  # Teal center circle
        painter.setPen(Qt.NoPen)
        inner_rect = self.rect().adjusted(100, 100, -100, -100)
        painter.drawEllipse(inner_rect)

    def start_spin(self, winning_slot):
        self.winning_slot = winning_slot
        self.highlight_slot = None
        slot_angle = 360 / 36

        # Center angle of winning slot
        slot_center_angle = (winning_slot - 1) * slot_angle + slot_angle / 2

        # Calculate stopping angle to align slot center at 90 degrees
        stop_at_angle = (360 * 5) + ((360 - slot_center_angle + 90) % 360)

        self.target_angle = stop_at_angle
        self.spins_remaining = self.target_angle
        self.rotation_angle = 0
        self.timer.start(10)
        self.update()

    def rotate(self):
        if self.spins_remaining > 0:
            step = min(self.spin_speed, self.spins_remaining)
            self.rotation_angle = (self.rotation_angle + step) % 360
            self.spins_remaining -= step
            self.update()
        else:
            self.timer.stop()
            self.highlight_slot = self.winning_slot
            self.update()
            self.highlight_timer.start(3000)  # Highlight for 3 seconds
            show_result()

    def clear_highlight(self):
        self.highlight_slot = None
        self.update()

# --- Layouts ---
layout1 = QVBoxLayout()
title = QLabel("Roulette")
title.setFont(QFont("Arial", 100))
title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
title.setStyleSheet("color: #FAFAFF;")  # Off white title text
layout1.addWidget(title)

tutorial = QLabel("Roulette is a casino game where players bet on where a ball will land on a spinning wheel.")
tutorial.setFont(QFont("Arial", 20))
tutorial.setAlignment(Qt.AlignLeft)
tutorial.setStyleSheet("color: #FAFAFF;")  # Off white tutorial text
layout1.addWidget(tutorial)

layout2 = QHBoxLayout()
layout3 = QVBoxLayout()
layout4 = QHBoxLayout()

# --- Betting UI ---
betting = QLineEdit("Your bet (must be a positive integer)")
betting.setFixedSize(300, 75)
betting.setAlignment(Qt.AlignCenter)
betting.setStyleSheet(f"""
    QLineEdit {{
        background-color: #38726C;  /* teal */
        color: #FAFAFF;             /* off white */
        font-size: 16px;
        border: 2px solid #72B01D; /* light green */
        border-radius: 8px;
        padding: 5px;
    }}
""")
layout4.addWidget(betting)

slot_input = QLineEdit("Your slot (1 - 36)")
slot_input.setFixedSize(300, 75)
slot_input.setAlignment(Qt.AlignCenter)
slot_input.setStyleSheet(f"""
    QLineEdit {{
        background-color: #38726C;  /* teal */
        color: #FAFAFF;             /* off white */
        font-size: 16px;
        border: 2px solid #72B01D; /* light green */
        border-radius: 8px;
        padding: 5px;
    }}
""")
layout4.addWidget(slot_input)

# --- Balance display ---
balance_display = QLabel(f"Balance: ${balance}")
balance_display.setFixedSize(600, 75)
balance_font = QFont("Arial", 24)
balance_font.setBold(True)  # Make font bold
balance_display.setFont(balance_font)
balance_display.setAlignment(Qt.AlignHCenter)  # Center horizontally
balance_display.setStyleSheet("color: #E03616;")  # red from palette
layout3.addWidget(balance_display)

layout3.addLayout(layout4, Qt.AlignTop)

# --- Confirm button ---
confirm_btn = QPushButton("Confirm your bet and slot")
confirm_btn.setFixedSize(600, 75)
confirm_btn.setStyleSheet(f"""
    QPushButton {{
        background-color: #E03616; /* red */
        color: #FAFAFF;            /* off white */
        font-size: 18px;
        border-radius: 10px;
    }}
    QPushButton:hover {{
        background-color: #72B01D; /* light green */
        color: #0D0A0B;            /* dark BG */
    }}
""")
layout3.addWidget(confirm_btn)

confirm_txt = QLabel("Everything you confirmed will be here")
confirm_txt.setFixedSize(600, 75)
confirm_txt.setFont(QFont("Arial", 20))
confirm_txt.setAlignment(Qt.AlignCenter)
confirm_txt.setStyleSheet("color: #FAFAFF;")  # off white
layout3.addWidget(confirm_txt)

# --- Wheel ---
wheel = RouletteWheel()

# --- Logic ---
def balance_func(bl: int, bet: int) -> int:
    return bl - bet

slot_list = [str(i + 1) for i in range(36)]
result = {"winning_slot": None, "player_slot": None, "bet_amount": 0}

def show():
    global balance
    current_bet = betting.text()
    current_slot = slot_input.text()

    if current_bet.isdigit() and current_slot in slot_list:
        bet_amount = int(current_bet)
        if bet_amount > balance or bet_amount <= 0:
            confirm_txt.setText("Insufficient balance or invalid bet.")
        else:
            result["bet_amount"] = bet_amount
            result["player_slot"] = int(current_slot)
            result["winning_slot"] = random.randint(1, 36)

            confirm_txt.setText(f"${bet_amount} on slot {current_slot}. Spinning...")
            wheel.start_spin(result["winning_slot"])
    else:
        confirm_txt.setText("Invalid input.")

    betting.setText("Your bet (must be a positive integer)")
    slot_input.setText("Your slot (1 - 36)")

def show_result():
    global balance
    if result["player_slot"] == result["winning_slot"]:
        win_amount = result["bet_amount"] * 36
        balance += win_amount
        confirm_txt.setText(f"🎉 You WON! Slot {result['winning_slot']}. You earned ${win_amount}")
    else:
        balance -= result["bet_amount"]
        confirm_txt.setText(f"❌ You lost. Winning slot: {result['winning_slot']}")

    balance_display.setText(f"Balance: ${balance}")

confirm_btn.clicked.connect(show)

# --- Layout setup ---
layout3_widget = QWidget()
layout3_widget.setLayout(layout3)
layout3_widget.setFixedWidth(600)

wheel_container = QVBoxLayout()
wheel_container.addWidget(wheel, alignment=Qt.AlignCenter)

layout2.addWidget(layout3_widget, alignment=Qt.AlignLeft)
layout2.addLayout(wheel_container)
layout1.addLayout(layout2)

window.setLayout(layout1)
# window.show()

# --- Run ---
sys.exit(app.exec_())
