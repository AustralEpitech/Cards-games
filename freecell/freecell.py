#!/usr/bin/env python3
import pygame as pg
import random

ASSETS = [
    "../assets/cards.png"
]

NUMBERS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
COLORS = ['H', 'C', 'D', 'S']

class Card:
    def __init__(self, surface: pg.surface, number: str, color: str):
        try:
            self.value = number + color
            self.surface = surface
            self.rect = pg.Rect(
                NUMBERS.index(number) * 81,
                COLORS.index(color) * 117,
                81,
                117
            )
        except Exception as e:
            print(f"{number + color}\n{e}")
            exit(1)

def initCards(surface: pg.Surface, seed = None, shuffle = True) -> list[Card]:
    deck = [[] for i in range(8)]

    if not seed:
        cards = [Card(surface, nb, color) for color in COLORS for nb in NUMBERS]
        if shuffle:
            random.shuffle(cards)
    else:
        cards = [Card(sprite, card[0], card[1]) for card in seed.split(" ")]
    for col in deck[:4]:
        for i in range(7):
            col.append(cards.pop())
    for col in deck[4:]:
        for i in range(6):
            col.append(cards.pop())
    return deck

def checkEvents():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

def main():
    window = pg.display.set_mode((800, 600), flags = pg.RESIZABLE)
    cardsIMG = pg.image.load(ASSETS[0])
    cards = initCards(cardsIMG)

    while 1:
        checkEvents()
        for i, col in enumerate(cards):
            for j, card in enumerate(col):
                window.blit(card.surface, (i * 91, j * 117 / 2), card.rect)
        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
