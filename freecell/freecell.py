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

def check_multiple_grab(cards: list[ce.Card]) -> list[ce.Card]:
    for i, card in enumerate(cards[1:], start = 1):
        if card.col % 2 == cards[i - 1].col % 2 or card.nb != cards[i - 1].nb - 1:
            return []
    return cards


def get_cards(pos: (int, int)) -> list[ce.Card]:
    if ce.is_y(ce.CELLS[0]["pos"][1], pos[1]):
        for el in ce.CELLS:
            if el["card"] and ce.is_x(el["pos"][0], pos[0]):
                return [el["card"]]
    for c in ce.CASCADES:
        if not c["cards"]:
            return []
        if not ce.is_x(c["cards"][0].pos[0], pos[0]):
            continue
        for i, card in enumerate(reversed(c["cards"])):
            if i > ce.MAXMOV:
                return []
            if ce.is_y(card.pos[1], pos[1]):
                return check_multiple_grab(c["cards"][len(c["cards"]) - i - 1:])
        return []
    return []


# TODO: calculate number of cards movable with empty cascades
def check_cells(card: ce.Card, pos: (int, int)) -> int:
    for el in ce.CELLS:
        if not ce.is_x(el["pos"][0], pos[0]):
            continue
        if not el["card"]:
            el["card"] = card.set_status(1, el["pos"])
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


def check_cascades(cards: list[ce.Card], pos: (int, int)) -> int:
    for el in ce.CASCADES:
        if not ce.is_x(el["pos"][0], pos[0]):
            continue
        if not el["cards"] or \
                (el["cards"][-1].col % 2 != cards[0].col % 2 and \
                el["cards"][-1].nb == cards[0].nb + 1):
            for i, card in enumerate(cards):
                el["cards"].append(card.set_status(0,
                    (el["pos"][0], el["pos"][1] + len(el["cards"]) * ce.CSPACE)))
            return 1
    return 0


def check_events(cards: list[ce.Card]) -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                ce.new_game(ce.SEED)
            elif event.key == pg.K_t:
                ce.new_game(None)
            #elif event.key == pg.K_SPACE:
            #    print(f"cards = {cards}\ncascades =")
            #    for cascade in ce.CASCADES:
            #        print(f"{cascade['cards']}")
        elif event.type == pg.MOUSEBUTTONDOWN and event.__dict__["button"] == 1:
            cards = get_cards(pg.mouse.get_pos())
        elif event.type == pg.MOUSEBUTTONUP and event.__dict__["button"] == 1 and cards:
            pos = pg.mouse.get_pos()

            if len(cards) > 1 or not ce.is_y(ce.CELLS[0]["pos"][1], pos[1]):
                check_cascades(cards, pos)
            else:
                check_cells(cards[0], pos) or check_piles(cards[0], pos)
            for i, card in enumerate(cards):
                card.pos = card.prev_pos
            cards = []
    return cards


# TODO: fix order of display if multiple cards moved
def display_game(cards: list[ce.Card], cells_rect: pg.rect, piles_rect: pg.rect):
    mouse_pos = pg.mouse.get_pos()
    pos = (mouse_pos[0] - ce.CSIZE[0] / 2, mouse_pos[1] - ce.CSPACE * 0.75)

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
    while True:
        cards = check_events(cards)
        display_game(cards, cells_rect, piles_rect)
    pg.quit()


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
