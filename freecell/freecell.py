#!/usr/bin/env python3
import os
import random
import sys
import pygame as pg

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS = {
    "bg": os.path.join(ASSETS_DIR, "backgrounds_stacks.png"),
    "cards": os.path.join(ASSETS_DIR, "cards.png"),
}

CARDSIZE = (133, 200)
CARDSPACE = CARDSIZE[1] * 0.325
PADDING = 0.1 * CARDSIZE[0]
WINDOWSIZE = (8 * (CARDSIZE[0] + PADDING) + PADDING, 15 * CARDSPACE)
maxMov = 1

NUMBERS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
COLORS = ['H', 'C', 'D', 'S']

class Card:
    value = ('', '')
    surface = 0
    pos = (0, 0)
    rect = (0, 0, 0, 0)

    def __init__(self, surface: pg.surface, number: str, col: str):
        self.value = (number, col)
        self.surface = surface
        try:
            self.rect = pg.Rect(
                NUMBERS.index(number) * CARDSIZE[0],
                COLORS.index(col) * CARDSIZE[1],
                CARDSIZE[0],
                CARDSIZE[1]
            )
        except Exception as e:
            print(f"ERROR: Card index does not exist")
            exit(1)

    def setCascadePos(self, x: int, y: int):
        self.pos = (x * (CARDSIZE[0] + PADDING) + PADDING,
                    CARDSIZE[1] + 2 * PADDING + y * CARDSPACE)

    def setPos(self, pos: (int, int)):
        self.pos = pos

    def getPos(self) -> (int, int):
        return (self.pos[0], self.pos[1])

    def isBTWX(self, x: int) -> bool:
        return self.pos[0] <= x <= self.pos[0] + self.rect[2]

    def isBTWY(self, y: int) -> bool:
        return self.pos[1] <= y <= self.pos[1] + self.rect[3]

    def isClicked(self, mousePos: (int, int)) -> bool:
        return isBTWX(mousePos[0]) and isBTWY(mousePos[1])

    def display(self, window: pg.display):
        window.blit(self.surface, self.pos, self.rect)

def getCard(cards: list[list[Card]], cells: list[Card], mousePos: (int, int)) -> (int, int):
    cascade = -1
    lenC = 0

    if PADDING <= mousePos[1] <= PADDING + CARDSIZE[0]:
        for i, cell in enumerate(cells):
            if i * (CARDSIZE[0] + PADDING) + PADDING <= mousePos[0] <= i * (CARDSIZE[0] + PADDING) + PADDING + CARDSIZE[0]:
                return i
    for i, el in enumerate(cards):
        if el[0].isBTWX(mousePos[0]):
            cascade = i
            break
    if cascade == -1:
        return None
    lenC = len(cards[cascade]) - 1
    for card in range(lenC, lenC - maxMov, -1):
        if cards[cascade][card].isBTWY(mousePos[1]):
            return (cascade, card)
    return None

def drawBG(bgIMG: pg.surface, window: pg.display, bgColor: (int, int, int)):
    window.fill(bgColor)
    for i in range(4):
        window.blit(
            bgIMG,
            (i * (CARDSIZE[0] + PADDING) + PADDING, PADDING),
            (0, 0, CARDSIZE[0], CARDSIZE[1])
        )
    for i in range(4, 8):
        window.blit(
            bgIMG,
            (i * (CARDSIZE[0] + PADDING) + PADDING, PADDING),
            (CARDSIZE[0] * 2, 0, CARDSIZE[0], CARDSIZE[1])
        )

def checkEvents(cards: list, cells: list, idx: (int, int)) -> (int, int):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                return -1
            if event.key == pg.K_t:
                return -2
        elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
            idx = getCard(cards, cells, pg.mouse.get_pos())
            if type(idx) == int:
                if not cells[idx]:
                    return None
                return idx
            if idx == None or idx[1] != len(cards[idx[0]]) - 1:
                return None
        elif event.type == pg.MOUSEBUTTONUP and idx != None and not pg.mouse.get_pressed()[0]:
            newIDX = getCard(cards, cells, pg.mouse.get_pos())
            if type(newIDX) == int:
                if cells[newIDX]:
                    if type(idx) == int:
                        cells[idx].setPos((idx * (CARDSIZE[0] + PADDING) + PADDING, PADDING))
                    else:
                        cards[idx[0]][idx[1]].setCascadePos(idx[0], idx[1])
                    return None
                if type(idx) == int:
                    cells[newIDX] = cells[idx]
                    cells[idx] = None
                else:
                    cells[newIDX] = cards[idx[0]].pop()
                cells[newIDX].setPos((newIDX * (CARDSIZE[0] + PADDING) + PADDING, PADDING))
                return None
            if type(idx) == int:
                card = cells[idx]
            else:
                card = cards[idx[0]][idx[1]]
            if newIDX != None and                                                                               \
                    NUMBERS.index(cards[newIDX[0]][newIDX[1]].value[0]) == NUMBERS.index(card.value[0]) + 1 and \
                    COLORS.index(cards[newIDX[0]][newIDX[1]].value[1]) % 2 != COLORS.index(card.value[1]) % 2:
                card.setCascadePos(newIDX[0], len(cards[newIDX[0]]))
                if type(idx) == int:
                    cells[idx] = None
                else:
                    cards[idx[0]].pop()
                cards[newIDX[0]].append(card)
            else:
                if type(idx) == int:
                    cells[idx].setPos((idx * (CARDSIZE[0] + PADDING) + PADDING, PADDING))
                else:
                    cards[idx[0]][idx[1]].setCascadePos(idx[0], idx[1])
            return None
    return idx

def initCards(surface: pg.Surface, seed: str) -> list[Card]:
    try:
        deck = [[] for i in range(8)]
        cards = [Card(surface, card[0], card[1]) for card in seed.split(" ")]

        for i, cascade in enumerate(deck[:4]):
            for j in range(7):
                cascade.append(cards.pop(0))
                cascade[-1].setCascadePos(i, j)
        for i, cascade in enumerate(deck[4:]):
            for j in range(6):
                cascade.append(cards.pop(0))
                cascade[-1].setCascadePos(i + 4, j)
        return deck
    except:
        print("ERROR: wrong seed")
        exit(1)

def getNewSeed():
    cards = [nb + color for color in COLORS for nb in NUMBERS]
    maxIDX = len(cards) - 1
    seed = ""

    while maxIDX >= 0:
        seed += cards.pop(random.randint(0, maxIDX)) + " "
        maxIDX -= 1
    return seed[:len(seed) - 1]

def main():
    bgIMG = pg.image.load(ASSETS["bg"])
    cardsIMG = pg.image.load(ASSETS["cards"])
    window = pg.display.set_mode(WINDOWSIZE)
    seed = getNewSeed() if len(sys.argv) < 2 else sys.argv[1]
    cards = initCards(cardsIMG, seed)
    bgColor = (0x31, 0xA1, 0x27)
    idx = None
    cells = [None, None, None, None]
    piles = [None, None, None, None]

    while 1:
        idx = checkEvents(cards, cells, idx)
        if type(idx) == int and idx < 0:
            if idx == -2:
                seed = getNewSeed()
            cards = initCards(cardsIMG, seed)
            cells = [None, None, None, None]
            piles = [None, None, None, None]
            idx = None
        drawBG(bgIMG, window, bgColor)
        for cascade in cards:
            for card in cascade:
                card.display(window)
        for card in cells:
            if card:
                card.display(window)
        if idx != None:
            if type(idx) == int:
                cells[idx].setPos(pg.mouse.get_pos())
                cells[idx].display(window)
            else:
                cards[idx[0]][idx[1]].setPos(pg.mouse.get_pos())
                cards[idx[0]][idx[1]].display(window)
        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
