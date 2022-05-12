#!/usr/bin/env python3
import sys
import os
import pygame as pg

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import card_engine as ce

ASSETS = {
    "bg": os.path.join(   ce.ASSETS_DIR, "backgrounds_stacks.png"),
    "cards": os.path.join(ce.ASSETS_DIR, "cards.png")
}


#TODO: multiple cards
def get_cards(pos: (int, int)) -> list[ce.Card]:
    if ce.is_y(ce.CELLS[0]["pos"][1], pos[1]):
        for el in ce.CELLS:
            if el["card"] and ce.is_x(el["pos"][0], pos[0]):
                return [el["card"]]
    for c in ce.CASCADES:
        if ce.is_x(c["cards"][0].pos[0], pos[0]):
            if not c["cards"]:
                return None
            for i, card in enumerate(reversed(c["cards"])):
                if ce.is_y(card.pos[1], pos[1]) and len(c["cards"][i:]) <= ce.MAXMOV:
                    return c["cards"][i:]
            return None
    return None


def check_cells(card: ce.Card, pos: (int, int)) -> int:
    for el in ce.CELLS:
        if not ce.is_x(el["pos"][0], pos[0]):
            continue
        if not el["card"]:
            el["card"] = card.set_status(1, el["pos"])
            MAXMOV += 1
        return 1
    return 0


def check_piles(card: ce.Card, pos: (int, int)) -> int:
    for el in ce.PILES:
        if not ce.is_x(el["pos"][0], pos[0]):
            continue
        if not el["card"]:
            if card.nb == 0:
                el["card"] = card.set_status(2, el["pos"])
        elif el["card"].nb == card.nb - 1:
            el["card"] = card.set_status(2, el["pos"])
        return 1
    return 0


def check_cascades(card: ce.Card, pos: (int, int)) -> int:
    for el in ce.CASCADES:
        if not ce.is_x(el["pos"][0], pos[0]):
            continue
        if not el["cards"] or \
                (el["cards"][-1].col % 2 != card.col % 2 and \
                el["cards"][-1].nb == card.nb + 1):
            el["cards"].append(card.set_status(
                0, (el["pos"][0], el["pos"][1] + len(el["cards"]) * ce.CSPACE)))
        return 1
    return 0


def check_events(cards: list[ce.Card]) -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.__dict__["unicode"] == 'r':
                ce.new_game(ce.SEED)
            elif event.__dict__["unicode"] == 't':
                ce.new_game(None)
        elif event.type == pg.MOUSEBUTTONDOWN and event.__dict__["button"] == 1:
            cards = get_cards(pg.mouse.get_pos())
            print(cards)
            if cards:
                cards[0].prev_pos = cards[0].pos
        elif event.type == pg.MOUSEBUTTONUP and event.__dict__["button"] == 1 and cards:
            pos = pg.mouse.get_pos()

            if len(cards) > 1 or not ce.is_y(ce.CELLS[0]["pos"][1], pos[1]):
                check_cascades(card, pos)
            else:
                check_cells(card, pos) or check_piles(card, pos)
            for i, card in enumerate(cards):
                card.pos = (cards[0].prev_pos[0], prev_pos[1] + ce.CSPACE * i)
            cards = []


def display_game(cards: list[ce.Card], cells_rect: pg.rect, piles_rect: pg.rect):
    mouse_pos = pg.mouse.get_pos()
    pos = (mouse_pos[0] - ce.CSIZE[0] / 2, mouse_pos[1] - ce.CSIZE[1] / 2)

    ce.WINDOW.fill(ce.BGCOL)
    ce.draw_slots(ce.CELLS, cells_rect)
    ce.draw_slots(ce.PILES, piles_rect)
    ce.draw_cascades()
    for i, card in enumerate(cards):
        card.pos = (pos[0], pos[1] + ce.CSPACE * i)
        card.display()
    pg.display.flip()


def main(argc: int, argv: list[str]):
    cells_rect = pg.Rect(0, 0, ce.CSIZE[0], ce.CSIZE[1])
    piles_rect = pg.Rect(ce.CSIZE[0] * 2, 0, ce.CSIZE[0], ce.CSIZE[1])
    bg_col = (0x31, 0xA1, 0x27)
    cards = []

    ce.init(ASSETS, argv[1] if argc >= 2 else None, bg_col)
    while 1:
        check_events(cards)
        display_game(cards, cells_rect, piles_rect)
    pg.quit()


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
