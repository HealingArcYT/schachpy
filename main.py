import os
import sys
import math

import pygame

pygame.init()
size = width, height = 800, 800

FARBE_WEISS = 0
FARBE_SCHWARZ = 1

speed = [1, 2]
black = 0, 0, 0

FPS_CLOCK = pygame.time.Clock()

screen = pygame.display.set_mode(size)

font = pygame.font.Font('.\\FreeSansBold.ttf', 16)


class Figur:
    NAMES = ["koenig", "koenigin", "laeufer", "springer", "turm", "bauer"]

    type: str
    name: str
    image: pygame.Surface
    initial_pos: bool
    farbe: int

    possibilities: list[tuple[int, int]]

    def __init__(self, name, type, farbe: int):
        if type in self.NAMES:
            _n = self.NAMES.index(type)
            self.name = name
            self.type = type

            self.image = pygame.image.load(
                os.path.join("textures", type + ("_w" if farbe == 0 else "_s") + ".png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width / 8, height / 8))

            self.initial_pos = True
            self.farbe = farbe
            self.possibilities = []

    def update(self, feld: list[list]):
        self.possibilities = []
        for i in range(8):
            j = 0
            for j in range(8):
                if feld[i][j] == self:
                    break

            if feld[i][j] == self:
                break
        if self.type == "bauer":

            if self.farbe == 0:
                if self.initial_pos:
                    if 0 <= i - 1 <= 7:
                        if feld[i - 1][j] is None:
                            self.possibilities += [(0, -1)]
                            if 0 <= i - 2 <= 7:
                                if feld[i - 2][j] is None:
                                    self.possibilities += [(0, -2)]

                else:
                    if 0 <= i - 1 <= 7:
                        if feld[i - 1][j] is None:
                            self.possibilities += [(0, -1)]

                if 0 <= i - 1 <= 7 and 0 <= j - 1 <= 7:
                    if feld[i - 1][j - 1] is not None:
                        if feld[i - 1][j - 1].farbe != self.farbe:
                            self.possibilities += [(-1, -1)]
                if 0 <= i - 1 <= 7 and 0 <= j + 1 <= 7:
                    if feld[i - 1][j + 1] is not None:
                        if feld[i - 1][j + 1].farbe != self.farbe:
                            self.possibilities += [(1, -1)]

            if self.farbe == 1:
                if self.initial_pos:
                    if 0 <= i + 1 <= 7:
                        if feld[i + 1][j] is None:
                            self.possibilities += [(0, 1)]
                            if 0 <= i + 2 <= 7:
                                if feld[i + 2][j] is None:
                                    self.possibilities += [(0, 2)]

                else:
                    if 0 <= i + 1 <= 7:
                        if feld[i + 1][j] is None:
                            self.possibilities += [(0, 1)]

                if 0 <= i + 1 <= 7 and 0 <= j + 1 <= 7:
                    if feld[i + 1][j + 1] is not None:
                        if feld[i + 1][j + 1].farbe != self.farbe:
                            self.possibilities += [(1, 1)]
                if 0 <= i + 1 <= 7 and 0 <= j - 1 <= 7:
                    if feld[i + 1][j - 1] is not None:
                        if feld[i + 1][j - 1].farbe != self.farbe:
                            self.possibilities += [(-1, 1)]

        if self.type == "turm" or self.type == "koenigin":
            # hoch
            for k in range(1, 8):
                if 0 <= i - k <= 7:
                    if feld[i - k][j] is None:
                        self.possibilities += [(0, -k)]
                        continue

                    if feld[i - k][j].farbe != self.farbe:
                        self.possibilities += [(0, -k)]
                    break

            # runter
            for k in range(1, 8):
                if 0 <= i + k <= 7:
                    if feld[i + k][j] is None:
                        self.possibilities += [(0, k)]
                        continue

                    if feld[i + k][j].farbe != self.farbe:
                        self.possibilities += [(0, k)]
                    break

            # links
            for k in range(1, 8):
                if 0 <= j - k <= 7:
                    if feld[i][j - k] is None:
                        self.possibilities += [(-k, 0)]
                        continue

                    if feld[i][j - k].farbe != self.farbe:
                        self.possibilities += [(-k, 0)]
                    break

            # rechts
            for k in range(1, 8):
                if 0 <= j + k <= 7:
                    if feld[i][j + k] is None:
                        self.possibilities += [(k, 0)]
                        continue

                    if feld[i][j + k].farbe != self.farbe:
                        self.possibilities += [(k, 0)]
                    break

        if self.type == "springer":
            for a in (1, 2, -1, -2):
                for b in (1, 2, -1, -2):
                    if a == b:
                        continue

                    if a == -b:
                        continue

                    if 0 <= i + a <= 7 and 0 <= j + b <= 7:
                        if feld[i + a][j + b] is None or feld[i + a][j + b].farbe != self.farbe:
                            self.possibilities += [(b, a)]

        if self.type == "laeufer" or self.type == "koenigin":
            plus_plus = plus_minus = minus_plus = minus_minus = True
            for a in range(1, 8):
                for b in range(1, 8):
                    if a == b:
                        if 0 <= i + a <= 7 and 0 <= j + b <= 7 and plus_plus:
                            if feld[i + a][j + b] is None or feld[i + a][j + b].farbe != self.farbe:
                                self.possibilities += [(b, a)]
                            else:
                                plus_plus = False

                        if 0 <= i + a <= 7 and 0 <= j - b <= 7 and plus_minus:
                            if feld[i + a][j - b] is None or feld[i + a][j - b].farbe != self.farbe:
                                self.possibilities += [(-b, a)]
                            else:
                                plus_minus = False

                        if 0 <= i - a <= 7 and 0 <= j + b <= 7 and minus_plus:
                            if feld[i - a][j + b] is None or feld[i - a][j + b].farbe != self.farbe:
                                self.possibilities += [(b, -a)]
                            else:
                                minus_plus = False

                        if 0 <= i - a <= 7 and 0 <= j - b <= 7 and minus_minus:
                            if feld[i - a][j - b] is None or feld[i - a][j - b].farbe != self.farbe:
                                self.possibilities += [(-b, -a)]
                            else:
                                minus_minus = False

        if self.type == "koenig":
            for a in (1, 0, -1):
                for b in (1, 0, -1):
                    if not (a == b == 0):
                        if 0 <= i + a <= 7 and 0 <= j + b <= 7:
                            if feld[i + a][j + b] is None or feld[i + a][j + b].farbe != self.farbe:
                                self.possibilities += [(b, a)]


class GameState:
    STATES = ["laufend", "schach", "schachmatt", "gewonnen"]

    def __init__(self, state, advantage_player=-1):
        if state in self.STATES:
            self.state = state
            self.advantage_player = advantage_player
        else:
            raise ValueError(f"state must be one of {self.STATES} and cannot be {state}")


class Brett:
    feld: list[list[Figur | None]]

    def __init__(self):
        self.feld = [[None for _ in range(8)] for _ in range(8)]
        # schwarz oben
        # Turm
        self.feld[0][0] = Figur("turm_1_s", "turm", FARBE_SCHWARZ)

        # Springer
        self.feld[0][1] = Figur("springer_1_s", "springer", FARBE_SCHWARZ)

        # Laeufer
        self.feld[0][2] = Figur("laeufer_1_s", "laeufer", FARBE_SCHWARZ)

        # Koenig
        self.feld[0][3] = Figur("koenig_s", "koenig", FARBE_SCHWARZ)

        # Koenigin
        self.feld[0][4] = Figur("koenigin_s", "koenigin", FARBE_SCHWARZ)

        # Turm
        self.feld[0][7] = Figur("turm_2_s", "turm", FARBE_SCHWARZ)

        # Springer
        self.feld[0][6] = Figur("springer_2_s", "springer", FARBE_SCHWARZ)

        # Laeufer
        self.feld[0][5] = Figur("laeufer_2_s", "laeufer", FARBE_SCHWARZ)

        # Bauern
        for i in range(8):
            self.feld[1][i] = Figur(f"bauer_{i}_s", "bauer", FARBE_SCHWARZ)

        # weiß unten
        # Turm
        self.feld[7][0] = Figur("turm_1_w", "turm", FARBE_WEISS)

        # Springer
        self.feld[7][1] = Figur("springer_1_w", "springer", FARBE_WEISS)

        # Laeufer
        self.feld[7][2] = Figur("laeufer_1_w", "laeufer", FARBE_WEISS)

        # Koenig
        self.feld[7][3] = Figur("koenig_w", "koenig", FARBE_WEISS)

        # Koenigin
        self.feld[7][4] = Figur("koenigin_w", "koenigin", FARBE_WEISS)

        # Turm
        self.feld[7][7] = Figur("turm_2_w", "turm", FARBE_WEISS)

        # Springer
        self.feld[7][6] = Figur("springer_2_w", "springer", FARBE_WEISS)

        # Laeufer
        self.feld[7][5] = Figur("laeufer_2_w", "laeufer", FARBE_WEISS)

        # Bauern
        for i in range(8):
            self.feld[6][i] = Figur(f"bauer_{i}_w", "bauer", FARBE_WEISS)

    def move(self, initial, goal):
        if initial == goal:
            return
        cp = self.feld[initial[0]][initial[1]]
        if cp is None:
            return

        if self.feld[goal[0]][goal[1]] is not None and self.feld[initial[0]][initial[1]].farbe == self.feld[goal[0]][
            goal[1]].farbe:
            return

        cp.initial_pos = False
        self.feld[goal[0]][goal[1]] = cp
        self.feld[initial[0]][initial[1]] = None

    def test_won(self) -> GameState:
        """returns -1 if not won else number of player that won"""
        s_k = w_k = False

        for i in self.feld:
            for j in i:
                if j is not None:
                    if j.type == "koenig":
                        if j.farbe == 0:
                            w_k = True
                        if j.farbe == 1:
                            s_k = True

        if s_k and w_k:
            for i in range(len(self.feld)):
                for j in range(len(self.feld[i])):
                    if self.feld[i][j] is None:
                        continue
                    for k in self.feld[i][j].possibilities:
                        try:
                            if self.feld[i + k[0]][j + k[1]].type == "koenig":
                                koenig = self.feld[i + k[0]][j + k[1]]
                                possibilities = [(i + _[0], j + _[1]) for _ in koenig.possibilities]
                                testing = [False for _ in possibilities]
                                for l in range(len(possibilities)):
                                    for m in range(len(self.feld)):
                                        for n in range(len(self.feld[m])):
                                            if self.feld[m][n] is None:
                                                continue
                                            for o in self.feld[m][n].possibilities:
                                                if (m + o[0], n + o[1]) == possibilities[l]:
                                                    testing[l] = True

                                if testing == []:
                                    continue
                                if False not in testing:
                                    return GameState("schachmatt", koenig.farbe ^ 1)
                                return GameState("schach", koenig.farbe ^ 1)
                        except:
                            pass
            return GameState("laufend")

        if s_k and not w_k:
            return GameState("gewonnen", 1)
        return GameState("gewonnen", 0)


brett = Brett()
spieler_dran = 0
game_running = True

_x, _y, x, y = None, None, None, None

while True:
    for i in range(8):
        for j in range(8):
            if brett.feld[i][j] is not None:
                brett.feld[i][j].update(brett.feld)
    selection = [[False for _ in range(8)] for _ in range(8)]

    if (y, x) != (None, None):
        selection[y][x] = True
        for i in brett.feld[y][x].possibilities:
            if 0 <= y + i[1] <= 7 and 0 <= x + i[0] <= 7:
                selection[y + i[1]][x + i[0]] = True

    sel_color = 20, 150, 20

    gs = brett.test_won()
    if gs.state == "gewonnen" or gs.state == "schachmatt":
        pygame.display.set_caption(f"Spieler {'weiß' if spieler_dran == 1 else 'schwarz'} hat gewonnen")
        game_running = False
    elif gs.state == "schach":
        pygame.display.set_caption(f"Spieler {'weiß' if spieler_dran == 0 else 'schwarz'} steht im Schach")
    else:
        pygame.display.set_caption(f"Spieler {'weiß' if spieler_dran == 0 else 'schwarz'} ist dran")
    screen.fill((255, 255, 255))
    mousedown = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not game_running:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()
            if left:
                if (x, y) != (None, None):
                    _x, _y = pygame.mouse.get_pos()
                    _x = math.ceil(_x / (width / 8)) - 1
                    _y = math.ceil(_y / (width / 8)) - 1

                    if selection[_y][_x] and not (_x, _y) == (x, y):
                        brett.move((y, x), (_y, _x))
                        spieler_dran = 1 if spieler_dran == 0 else 0
                    else:
                        _x, _y = None, None
                if (_x, _y) == (None, None):
                    x, y = pygame.mouse.get_pos()
                    x = math.ceil(x / (width / 8)) - 1
                    y = math.ceil(y / (width / 8)) - 1

                    if (brett.feld[y][x] is None) or (brett.feld[y][x].farbe != spieler_dran):
                        x, y = None, None

                    else:
                        print(brett.feld[y][x].initial_pos, brett.feld[y][x].possibilities)

                else:
                    _x, _y, x, y = None, None, None, None
            if right:
                x, y = None, None

    for i in range(8):
        for j in range(8):
            outline_only = False
            rect = pygame.rect.Rect(j * math.ceil(width / 8), i * math.ceil(height / 8), math.ceil(width / 8),
                                    math.ceil(height / 8))
            if i % 2 == j % 2:
                color = (230, 255, 225)
            else:
                color = (50, 30, 25)

            __x, __y = pygame.mouse.get_pos()

            if j * math.ceil(width / 8) <= __x < j * math.ceil(width / 8) + math.ceil(width / 8) and i * math.ceil(
                    height / 8) <= __y < i * math.ceil(height / 8) + math.ceil(height / 8):
                color = 100, 200, 255

            if selection[i][j]:
                if color == (230, 255, 225):
                    color = 180, 255, 180

                if color == (50, 30, 25):
                    color = 0, 50, 0

                if color == (100, 200, 255):
                    color = 70, 200, 200

            pygame.draw.rect(screen, color, rect)

            if (i, j) == (y, x):
                pygame.draw.rect(screen, sel_color, rect, 3)

            if brett.feld[i][j] is not None:
                img = brett.feld[i][j].image
                rct = img.get_rect()

                rct.center = j * math.ceil(width / 8) + math.ceil(width / 16), i * math.ceil(height / 8) + math.ceil(
                    height / 16)

                screen.blit(img, rct)

    # fps_counter = font.render(str(FPS_CLOCK.get_fps()), True, (255, 200, 200))
    # fps_counter_rect = fps_counter.get_rect()
    # fps_counter_rect.center = fps_counter_rect.width//2, fps_counter_rect.height//2

    # screen.blit(fps_counter, fps_counter_rect)

    pygame.display.flip()
    FPS_CLOCK.tick(60)
