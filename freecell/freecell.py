#!/usr/bin/env python3
import sys
import os
import pygame as pg

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import cardEngine as ce

ASSETS = {
    "bg": os.path.join(   ce.ASSETS_DIR, "backgrounds_stacks.png"),
    "cards": os.path.join(ce.ASSETS_DIR, "cards.png")
}

#TODO: multiple cards
def getCard(pos: (int, int)) -> ce.Card:
    if ce.isY(ce.CELLS[0]["pos"][1], pos[1]):
        for el in ce.CELLS:
            if el["card"] and ce.isX(el["pos"][0], pos[0]):
                return el["card"]
    for c in ce.CASCADES:
        if ce.isX(c["cards"][0].pos[0], pos[0]):
            if not c["cards"] or not ce.isY(c["cards"][-1].pos[1], pos[1]):
                return None
            return c["cards"][-1]
    return None

def checkCells(card: ce.Card, pos: (int, int)) -> int:
    for el in ce.CELLS:
        if not ce.isX(el["pos"][0], pos[0]):
            continue
        if not el["card"]:
            el["card"] = card.setStatus(1, el["pos"])
        return 1
    return 0

def checkPiles(card: ce.Card, pos: (int, int)) -> int:
    for el in ce.PILES:
        if not ce.isX(el["pos"][0], pos[0]):
            continue
        if not el["card"]:
            if card.nb == 0:
                el["card"] = card.setStatus(2, el["pos"])
        elif el["card"].nb == card.nb - 1:
            el["card"] = card.setStatus(2, el["pos"])
        return 1
    return 0

def checkCascades(card: ce.Card, pos: (int, int)) -> int:
    for el in ce.CASCADES:
        if not ce.isX(el["pos"][0], pos[0]):
            continue
        if not el["cards"] or \
                (el["cards"][-1].col % 2 != card.col % 2 and \
                el["cards"][-1].nb == card.nb + 1):
            el["cards"].append(card.setStatus(
                0, (el["pos"][0], el["pos"][1] + len(el["cards"]) * ce.CSPACE)))
        return 1
    return 0

def checkEvents(card: ce.Card) -> ce.Card:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.__dict__["unicode"] == 'r':
                ce.newGame(ce.SEED)
            elif event.__dict__["unicode"] == 't':
                ce.newGame(None)
        elif event.type == pg.MOUSEBUTTONDOWN and event.__dict__["button"] == 1:
            card = getCard(pg.mouse.get_pos())
            if card:
                card.prevPos = card.pos
        elif event.type == pg.MOUSEBUTTONUP and event.__dict__["button"] == 1 and card:
            pos = pg.mouse.get_pos()

            if ce.isY(ce.CELLS[0]["pos"][1], pos[1]):
                checkCells(card, pos) or checkPiles(card, pos)
            else:
                checkCascades(card, pos)
            card.pos = card.prevPos
            card = None
    return card

def displayGame(card: ce.Card, cellsRect: pg.rect, pilesRect: pg.rect):
    ce.WINDOW.fill(ce.BGCOL)
    ce.drawSlots(ce.CELLS, cellsRect)
    ce.drawSlots(ce.PILES, pilesRect)
    ce.drawCascades()
    if card:
        card.display()
    pg.display.flip()

def main():
    cellsRect = pg.Rect(0, 0, ce.CSIZE[0], ce.CSIZE[1])
    pilesRect = pg.Rect(ce.CSIZE[0] * 2, 0, ce.CSIZE[0], ce.CSIZE[1])
    bgCol = (0x31, 0xA1, 0x27)
    card = None

    ce.init(ASSETS, sys.argv[1] if len(sys.argv) >= 2 else None, bgCol)
    while 1:
        card = checkEvents(card) # reset game
        if card:
            mousePos = pg.mouse.get_pos()
            pos = (mousePos[0] - ce.CSIZE[0] / 2, mousePos[1] - ce.CSIZE[1] / 2)
            card.pos = pos
        displayGame(card, cellsRect, pilesRect)
    pg.quit()

if __name__ == "__main__":
    main()
