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
    prevPos = (0, 0)
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
        for el in CELLS:
            if el["card"] == self:
                el["card"] = None

    def setStatus(self, status: int, pos: (int, int)):
        self.remove()
        self.pos = self.prevPos = pos
        self.status = status
        return self

    def display(self):
        WINDOW.blit(self.surface, self.pos, self.rect)

def isX(cardX: int, x: int) -> bool:
    return cardX <= x <= cardX + CSIZE[0]

def isY(cardY: int, y: int) -> bool:
    return cardY <= y <= cardY + CSIZE[1]

def isXY(cardPos: (int, int), pos: (int, int)) -> bool:
    return isX(cardPos[0], pos[0]) and isY(cardPos[0], pos[1])

def drawSlots(array: list, rect: pg.rect):
    for el in array:
        WINDOW.blit(TEXTURES["bg"], el["pos"], rect)
        if el["card"]:
            el["card"].display()

def drawCascades():
    for cascade in CASCADES:
        for card in cascade["cards"]:
            card.display()

def initCards():
    try:
        cards = [
            Card(TEXTURES["card"], NUMBERS.index(card[0]), COLORS.index(card[1]))
        for card in SEED.split(" ")]

        for cascade in CASCADES[:4]:
            for y in range(7):
                cards[0].pos = (cascade["pos"][0], cascade["pos"][1] + CSPACE * y)
                cascade["cards"].append(cards.pop(0))
        for cascade in CASCADES[4:]:
            for y in range(6):
                cards[0].pos = (cascade["pos"][0], cascade["pos"][1] + CSPACE * y)
                cascade["cards"].append(cards.pop(0))
    except:
        print("ERROR: Wrong seed")
        exit(1)

# TODO: error handling
def getNewSeed():
    cards = [nb + color for color in COLORS for nb in NUMBERS]
    maxIDX = len(cards) - 1
    seed = ""

    while maxIDX >= 0:
        seed += cards.pop(random.randint(0, maxIDX)) + " "
        maxIDX -= 1
    seed = seed[:-1]
    print(f"seed = \"{seed}\"")
    return seed

def newGame(seed: str):
    global SEED

    for el in CASCADES:
        el["cards"] = []
    for i, _ in enumerate(CELLS):
        CELLS[i]["card"] = PILES[i]["card"] = None
    SEED = seed or getNewSeed()
    initCards()

def init(assets: list[str], seed: str, bgCol: (int, int, int)):
    global WINDOW
    global BGCOL

    pg.init()
    WINDOW = pg.display.set_mode(WINDOWSIZE)
    BGCOL = bgCol
    TEXTURES["bg"] = pg.image.load(assets["bg"])
    TEXTURES["card"] = pg.image.load(assets["cards"])
    newGame(seed)
