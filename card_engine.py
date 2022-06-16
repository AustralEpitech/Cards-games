#!/usr/bin/env python3
import random
import os
import pygame as pg

CSIZE = (133, 200)
PADDING = int(0.1 * CSIZE[0])
XPADDING = CSIZE[0] + PADDING
YPADDING = CSIZE[1] + PADDING
CSPACE = int(CSIZE[1] * 0.325)

WINDOWSIZE = (8 * XPADDING + PADDING, 15 * CSPACE)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

NUMBERS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
COLORS = ['H', 'C', 'D', 'S']

TEXTURES = {
    "bg": None,
    "card": None
}

SEED = None
BGCOL = None
WINDOW = None

MAXMOV = 0

CASCADES = [
    {"cards": [], "pos": (i * XPADDING + PADDING, YPADDING + PADDING)}
for i in range(8)]

CELLS = [
    {"card": None, "pos": (i * XPADDING + PADDING, PADDING)}
for i in range(4)]

PILES = [
    {"card": None, "pos": (i * XPADDING + PADDING, PADDING)}
for i in range(4, 8)]


class Card:
    nb = 0
    col = 0
    surface = 0
    pos = (0, 0)
    prev_pos = (0, 0)
    rect = (0, 0, 0, 0)
    status = 0  # cascades, cells or piles


    def __init__(self, surface: pg.surface, nb: int, col: int):
        self.nb = nb
        self.col = col
        self.surface = surface
        self.rect = pg.Rect(nb * CSIZE[0], col * CSIZE[1], CSIZE[0], CSIZE[1])


    def remove(self):
        if self.status == 0:
            for cascade in CASCADES:
                if cascade["cards"][-1] == self:
                    cascade["cards"].pop()
                    return
        for el in CELLS:
            if el["card"] == self:
                el["card"] = None
                return


    def set_status(self, status: int, pos: (int, int)):
        global MAXMOV

        self.remove()
        self.pos = self.prev_pos = pos
        if self.status == 1:
            MAXMOV += 1
        self.status = status
        if status == 1:
            MAXMOV -= 1
        return self


    def display(self):
        WINDOW.blit(self.surface, self.pos, self.rect)


    def __repr__(self):
        return NUMBERS[self.nb] + COLORS[self.col]


def is_x(card_x: int, x: int) -> bool:
    return card_x <= x <= card_x + CSIZE[0]


def is_y(card_y: int, y: int) -> bool:
    return card_y <= y <= card_y + CSIZE[1]


def is_xy(card_pos: (int, int), pos: (int, int)) -> bool:
    return is_x(card_pos[0], pos[0]) and is_y(card_pos[0], pos[1])


def draw_slots(array: list, rect: pg.rect):
    for el in array:
        WINDOW.blit(TEXTURES["bg"], el["pos"], rect)
        if el["card"]:
            el["card"].display()


def draw_cascades():
    for cascade in CASCADES:
        for card in cascade["cards"]:
            card.display()


def init_cards():
    try:
        cards = [
            Card(TEXTURES["card"], NUMBERS.index(card[0]), COLORS.index(card[1]))
        for card in SEED.split(" ")]

        for cascade in CASCADES[:4]:
            for y in range(7):
                cards[0].pos = (cascade["pos"][0], cascade["pos"][1] + CSPACE * y)
                cards[0].prev_pos = cards[0].pos
                cascade["cards"].append(cards.pop(0))
        for cascade in CASCADES[4:]:
            for y in range(6):
                cards[0].pos = (cascade["pos"][0], cascade["pos"][1] + CSPACE * y)
                cards[0].prev_pos = cards[0].pos
                cascade["cards"].append(cards.pop(0))
    except:
        print("ERROR: Wrong seed")
        sys.exit(1)

# TODO: error handling
def get_new_seed() -> None:
    cards = [nb + color for color in COLORS for nb in NUMBERS]
    max_idx = len(cards) - 1
    seed = ""

    while max_idx >= 0:
        seed += cards.pop(random.randint(0, max_idx)) + " "
        max_idx -= 1
    seed = seed[:-1]
    print(f"seed = \"{seed}\"")
    return seed


def new_game(seed: str) -> None:
    global SEED
    global MAXMOV

    for el in CASCADES:
        el["cards"] = []
    for i, _ in enumerate(CELLS):
        CELLS[i]["card"] = PILES[i]["card"] = None
    SEED = seed or get_new_seed()
    MAXMOV = 4
    init_cards()


def init(assets: list[str], seed: str, bg_col: (int, int, int)) -> None:
    global WINDOW
    global BGCOL

    pg.init()
    WINDOW = pg.display.set_mode(WINDOWSIZE)
    BGCOL = bg_col
    TEXTURES["bg"] = pg.image.load(assets["bg"])
    TEXTURES["card"] = pg.image.load(assets["cards"])
    new_game(seed)
