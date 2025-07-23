import sys
import random
import math
from PyQt5.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsRectItem,
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPainter
# from main_gui import *

# Constants
WIDTH, HEIGHT = 800, 600
PEG_RADIUS = 5
BALL_RADIUS = 8
GRAVITY = 0.15
NUM_BINS = 12
BIN_WIDTH = WIDTH // NUM_BINS
BIN_HEIGHT = 100
PEG_SPACING_X = 60
PEG_SPACING_Y = 60
OFFSET_X = WIDTH // 2
OFFSET_Y = 100

prize_multipliers = [10, 5, 2, 1, 0.5, 0.5, 0.5, 0.5, 1, 2, 5, 1000]
prize_values = [f"${m}x" for m in prize_multipliers]

class Ball:
    def __init__(self, scene, bet_amount):
        self.scene = scene
        self.x = WIDTH / 2
        self.y = 50
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = 0
        self.finished = False
        self.bet = float(bet_amount)
        self.winnings = 0
        self.item = QGraphicsEllipseItem(self.x, self.y, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.item.setBrush(QColor(255, 0, 0))
        self.scene.addItem(self.item)

    def update(self, pegs):
        if self.finished:
            return

        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

        for peg in pegs:
            peg_center_x = peg.x() + PEG_RADIUS
            peg_center_y = peg.y() + PEG_RADIUS

            dx = self.x + BALL_RADIUS - peg_center_x
            dy = self.y + BALL_RADIUS - peg_center_y
            distance = math.hypot(dx, dy)
            min_dist = PEG_RADIUS + BALL_RADIUS

            if distance < min_dist and distance > 0:
                # Simulate pyramid-style bounce
                if dx < 0:
                    self.vx = -abs(random.uniform(1.0, 2.0))  # bounce left
                else:
                    self.vx = abs(random.uniform(1.0, 2.0))   # bounce right

                self.vy = random.uniform(0.5, 1.5)
                self.y += 1  # push away slightly to avoid sticking
                break

        if self.y >= HEIGHT - BIN_HEIGHT:
            bin_index = min(range(NUM_BINS), key=lambda i: abs(self.x - (i * BIN_WIDTH + BIN_WIDTH / 2)))
            self.winnings = self.bet * prize_multipliers[bin_index]
            self.finished = True

        self.item.setRect(self.x, self.y, BALL_RADIUS * 2, BALL_RADIUS * 2)

class PlinkoGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plinko Game - PyQt5")
        self.setGeometry(550,100,0,0)
        self.scene = QGraphicsScene(0, 0, WIDTH, HEIGHT)
        self.scene.setBackgroundBrush(QColor(20, 20, 40))  # Blue background
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setFixedSize(WIDTH + 2, HEIGHT + 2)

        self.balance = 100.00
        self.bet_amount = 10.00
        self.balls = []
        self.pegs = []
        self.total_winnings = 0
        
        self.input = QLineEdit(str(self.bet_amount))
        self.balance_label = QLabel()
        self.bet_label = QLabel()
        self.winnings_label = QLabel()
        self.warning_label = QLabel()
        self.drop_button = QPushButton("Drop Ball")
        self.play_button = QPushButton("Play Again")

        self.drop_button.clicked.connect(self.drop_ball)
        self.play_button.clicked.connect(self.restart_game)
        self.play_button.setVisible(False)

        self.setup_ui()
        self.draw_pegs()
        self.draw_bins()

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

    def setup_ui(self):
        font = QFont()
        font.setPointSize(12)

        self.input.setFont(font)
        self.balance_label.setFont(font)
        self.bet_label.setFont(font)
        self.winnings_label.setFont(font)
        self.warning_label.setFont(font)
        self.warning_label.setStyleSheet("color: red")
        self.drop_button.setFont(font)
        self.play_button.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.balance_label)
        layout.addWidget(self.bet_label)
        layout.addWidget(self.winnings_label)
        layout.addWidget(self.warning_label)

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Bet Amount:"))
        input_layout.addWidget(self.input)
        layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.drop_button)
        button_layout.addWidget(self.play_button)
        layout.addLayout(button_layout)

        #main screen button
        self.button_mainScreen = QPushButton("Back to main screen")
        layout.addWidget(self.button_mainScreen)

        self.setLayout(layout)
        self.update_labels()

    def draw_pegs(self):
        for row in range(12):
            for col in range(row + 1):
                x = OFFSET_X + (col - row / 2) * PEG_SPACING_X
                y = OFFSET_Y + row * PEG_SPACING_Y
                peg = QGraphicsEllipseItem(x, y, PEG_RADIUS * 2, PEG_RADIUS * 2)
                peg.setBrush(QColor(255, 255, 255))
                self.scene.addItem(peg)
                self.pegs.append(peg)

    def draw_bins(self):
        for i in range(NUM_BINS):
            x = i * BIN_WIDTH
            bin_rect = QGraphicsRectItem(x, HEIGHT - BIN_HEIGHT, BIN_WIDTH, BIN_HEIGHT)
            bin_rect.setBrush(QColor(200, 200, 255))
            self.scene.addItem(bin_rect)

            label = self.scene.addText(prize_values[i])
            label.setDefaultTextColor(QColor(255, 255, 0))
            label.setPos(x + BIN_WIDTH / 4, HEIGHT - BIN_HEIGHT / 2)

    def update_labels(self):
        self.balance_label.setText(f"Balance: ${self.balance:.2f}")
        self.bet_label.setText(f"Bet: ${self.input.text()}")
        self.winnings_label.setText(f"Total Winnings: ${self.total_winnings:.2f}")

    def drop_ball(self):
        try:
            bet = float(self.input.text())
            if self.balance >= bet:
                self.balance -= bet
                self.balls.append(Ball(self.scene, bet))
                self.warning_label.setText("")
                self.play_button.setVisible(False)
            else:
                self.warning_label.setText("Insufficient Balance!")
        except:
            self.warning_label.setText("Invalid Bet Amount!")

        self.update_labels()

    def restart_game(self):
        for ball in self.balls:
            self.scene.removeItem(ball.item)
        self.balls.clear()
        self.total_winnings = 0
        self.warning_label.setText("")
        self.play_button.setVisible(False)
        self.update_labels()

    def game_loop(self):
        for ball in self.balls:
            ball.update(self.pegs)

        for ball in self.balls:
            if ball.finished and ball.winnings > 0:
                self.balance += ball.winnings
                self.total_winnings += ball.winnings
                ball.winnings = 0
                self.update_labels()
                self.play_button.setVisible(True)

    

        

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     game = PlinkoGame()
#     game.show()
#     sys.exit(app.exec_())
