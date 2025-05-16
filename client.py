from math import hypot
from socket import socket, AF_INET, SOCK_STREAM
from PyQt5.QtWidgets import QApplication
from pygame import *
from threading import Thread
from random import randint
from launcher import GameLauncher

app = QApplication([])
launcher = GameLauncher()
launcher.show()
app.exec()

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((launcher.host, int(launcher.port)))
my_data = list(map(int, sock.recv(64).decode().strip().split(',')))
my_id = my_data[0]
my_player = my_data[1:]
sock.setblocking(False)
name = launcher.name

init()
window = display.set_mode((1000, 1000))
clock = time.Clock()
f = font.Font(None, 50)
name_font = font.Font(None, 30)
all_players = []
running = True
lose = False

# Завантажуємо фото гравця, якщо вибране
player_image = None
if launcher.photo_path:
    try:
        player_image = image.load(launcher.photo_path).convert_alpha()
    except Exception as e:
        print(f"Не вдалося завантажити фото: {e}")

def receive_data():
    global all_players, running, lose
    while running:
        try:
            data = sock.recv(4096).decode().strip()
            if data == "LOSE":
                lose = True
            elif data:
                parts = data.strip('|').split('|')
                all_players = [list(map(int, p.split(',')[:4])) + [p.split(',')[-1]] for p in parts if len(p.split(',')) == 5]
        except:
            pass

Thread(target=receive_data, daemon=True).start()

class Eat:
    def __init__(self, x, y, r, c):
        self.x = x
        self.y = y
        self.radius = r
        self.color = c

    def check_collision(self, player_x, player_y, player_r):
        dx = self.x - player_x
        dy = self.y - player_y
        return hypot(dx, dy) <= self.radius + player_r

eats = [Eat(randint(-20000, 20000), randint(-20000, 20000), 10,
            (randint(0, 255), randint(0, 255), randint(0, 255)))
        for _ in range(10000)]

def draw_grid(surface, width, height, cell_size, player_pos, scale, color=(220, 220, 220)):
    px, py = player_pos
    start_x = -((px * scale) % cell_size)
    start_y = -((py * scale) % cell_size)

    for x in range(int(start_x), width, cell_size):
        draw.line(surface, color, (x, 0), (x, height))
    for y in range(int(start_y), height, cell_size):
        draw.line(surface, color, (0, y), (width, y))

def make_round_image(img, radius):
    size = radius * 2
    rounded = Surface((size, size), SRCALPHA)
    draw.circle(rounded, (255, 255, 255), (radius, radius), radius)
    img = transform.smoothscale(img, (size, size))
    img.set_colorkey((0, 0, 0))
    rounded.blit(img, (0, 0), special_flags=BLEND_RGBA_MIN)
    return rounded

player_image = None
if launcher.photo_path:
    try:
        img = image.load(launcher.photo_path).convert_alpha()
        player_image = make_round_image(img, int(my_player[2]))
    except Exception as e:
        print(f"Не вдалося завантажити фото: {e}")

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    window.fill((255, 255, 255))
    scale = max(0.3, min(50 / my_player[2], 1.5))
    draw_grid(window, 1000, 1000, int(64 * scale), (my_player[0], my_player[1]), scale)

    for p in all_players:
        if p[0] == my_id:
            continue
        sx = int((p[1] - my_player[0]) * scale + 500)
        sy = int((p[2] - my_player[1]) * scale + 500)
        draw.circle(window, (255, 0, 0), (sx, sy), int(p[3] * scale))
        name_text = name_font.render(p[4], 1, (0, 0, 0))
        window.blit(name_text, (sx, sy))

    center_x, center_y = 500, 500
    radius_scaled = int(my_player[2] * scale)

    if player_image:
        img_scaled = make_round_image(player_image, radius_scaled)
        img_rect = img_scaled.get_rect(center=(center_x, center_y))
        window.blit(img_scaled, img_rect)
    else:
        draw.circle(window, (0, 255, 0), (center_x, center_y), radius_scaled)

    to_remove = []
    for eat in eats:
        if eat.check_collision(my_player[0], my_player[1], my_player[2]):
            to_remove.append(eat)
            my_player[2] += int(eat.radius * 0.2)
        else:
            sx = int((eat.x - my_player[0]) * scale + 500)
            sy = int((eat.y - my_player[1]) * scale + 500)
            draw.circle(window, eat.color, (sx, sy), int(eat.radius * scale))

    for eat in to_remove:
        eats.remove(eat)
        if len(eats) <= 40:
            eats = [Eat(randint(-20000, 20000), randint(-20000, 20000), 10,
                        (randint(0, 255), randint(0, 255), randint(0, 255)))
                    for _ in range(10000)]


    if lose:
        t = f.render('U lose!', 1, (244, 0, 0))
        window.blit(t, (400, 500))

    display.update()
    clock.tick(60)

    if not lose:
        keys = key.get_pressed()
        if keys[K_w]: my_player[1] -= 15
        if keys[K_s]: my_player[1] += 15
        if keys[K_a]: my_player[0] -= 15
        if keys[K_d]: my_player[0] += 15

        try:
            msg = f"{my_id},{my_player[0]},{my_player[1]},{my_player[2]},{name}"
            sock.send(msg.encode())
        except:
            pass

quit()
