import pygame
import random
import math
import time

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Plinko Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_BG = (20, 20, 40)
YELLOW = (255, 255, 0)
BRIGHT_SLOT = (200, 200, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)
WARNING_COLOR = (255, 100, 100)

# Peg settings
PEG_RADIUS = 5
PEG_SPACING_X = 60
PEG_SPACING_Y = 60
OFFSET_X = WIDTH // 2
OFFSET_Y = 100

# Ball settings
BALL_RADIUS = 8
BALL_COLOR = RED
GRAVITY = 0.15
BOUNCE_DAMPENING = 0.4

# Bin settings
NUM_BINS = 12
BIN_WIDTH = WIDTH // NUM_BINS
BIN_HEIGHT = 100
prize_multipliers = [10, 5, 2, 1, 0.5, 0.5, 0.5, 0.5, 1, 2, 5, 1000]
prize_values = [f"${multiplier}x" for multiplier in prize_multipliers]

# Betting and balance
bet_amount = "10.00"
user_text = bet_amount
balance = 100.00
input_active = False
insufficient_funds = False

# Play Again Button
BUTTON_WIDTH, BUTTON_HEIGHT = 140, 40
button_rect = pygame.Rect(WIDTH - BUTTON_WIDTH - 20, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
font_button = pygame.font.Font(None, 30)

# Peg positions
pegs = []
for row in range(12):
    for col in range(row + 1):
        x = OFFSET_X + (col - row / 2) * PEG_SPACING_X
        y = OFFSET_Y + row * PEG_SPACING_Y
        pegs.append((x, y))

# Ball class
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 50
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = 0
        self.finished = False
        self.winnings = 0
        self.start_time = time.time()
        self.elapsed_time = 0

    def update(self):
        if self.finished:
            return

        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

        for peg in pegs:
            if math.hypot(self.x - peg[0], self.y - peg[1]) < PEG_RADIUS + BALL_RADIUS:
                self.vy *= -BOUNCE_DAMPENING
                self.vx = random.uniform(-1.5, 1.5)
                self.y -= 5

        if self.y >= HEIGHT - BIN_HEIGHT:
            bin_index = min(range(NUM_BINS), key=lambda i: abs(self.x - (i * BIN_WIDTH + BIN_WIDTH // 2)))
            self.winnings = float(bet_amount) * prize_multipliers[bin_index]
            self.elapsed_time = time.time() - self.start_time
            self.finished = True

    def draw(self):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)

def draw_pegs():
    for peg in pegs:
        pygame.draw.circle(screen, WHITE, peg, PEG_RADIUS)

def draw_bins():
    for i in range(NUM_BINS):
        x = i * BIN_WIDTH
        pygame.draw.rect(screen, BRIGHT_SLOT, (x, HEIGHT - BIN_HEIGHT, BIN_WIDTH, BIN_HEIGHT))
        font = pygame.font.Font(None, 24)
        text = font.render(prize_values[i], True, YELLOW)
        screen.blit(text, (x + BIN_WIDTH // 4, HEIGHT - BIN_HEIGHT // 2))

def display_info(total_winnings):
    font = pygame.font.Font(None, 36)
    balance_text = font.render(f"Balance: ${balance:.2f}", True, WHITE)
    bet_text = font.render(f"Bet: ${user_text}", True, WHITE)
    winnings_text = font.render(f"Total Winnings: ${total_winnings:.2f}", True, YELLOW)

    screen.blit(balance_text, (WIDTH // 2 - 80, 10))
    screen.blit(bet_text, (WIDTH // 2 - 70, 40))
    screen.blit(winnings_text, (WIDTH // 2 - 120, 70))

    if insufficient_funds:
        warning = font.render("Insufficient Balance!", True, WARNING_COLOR)
        screen.blit(warning, (WIDTH // 2 - 120, 110))

def draw_play_again_button():
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect, border_radius=8)
    text = font_button.render("Play Again", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def main():
    global balance, user_text, bet_amount, input_active, insufficient_funds
    clock = pygame.time.Clock()
    balls = []
    total_winnings = 0

    running = True
    while running:
        screen.fill(DARK_BG)
        draw_pegs()
        draw_bins()

        for ball in balls:
            ball.update()
            ball.draw()

        # Add winnings to balance once ball finishes
        for ball in balls:
            if ball.finished and ball.winnings > 0:
                balance += ball.winnings
                total_winnings += ball.winnings
                ball.winnings = 0

        display_info(total_winnings)

        if balls and all(ball.finished for ball in balls):
            draw_play_again_button()

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Right-click to drop another ball
                if event.button == 3:
                    try:
                        bet_val = float(bet_amount)
                        if balance >= bet_val:
                            balance -= bet_val
                            balls.append(Ball())
                            insufficient_funds = False
                        else:
                            insufficient_funds = True
                    except:
                        pass

                # Left-click to restart (Play Again button)
                elif event.button == 1 and balls and all(ball.finished for ball in balls):
                    balls.clear()
                    total_winnings = 0
                    insufficient_funds = False

                elif not input_active:
                    input_active = True
                    user_text = ""

            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if user_text.replace(".", "").isdigit():
                            bet_amount = user_text
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

                # Press R to play again
                if event.key == pygame.K_r and balls and all(ball.finished for ball in balls):
                    balls.clear()
                    total_winnings = 0
                    insufficient_funds = False

    pygame.quit()

if __name__ == "__main__":
    main()
