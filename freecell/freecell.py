#!/usr/bin/env python3
import random

numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
colors = ['H', 'C', 'D', 'S']

class Card:
    def __init__(self, number: str, col: str):
        if not number in numbers or not col in colors:
            return None
        self.value = number + col

def initCards(seed = None, shuffle = True) -> list[Card]:
    deck = [[] for i in range(8)]

    if not seed:
        cards = [Card(nb, col) for col in colors for nb in numbers]
        if shuffle:
            random.shuffle(cards)
    else:
        cards = [Card(card[0], card[1]) for card in seed.split(" ")]
    for col in deck[:4]:
        for i in range(7):
            col.append(cards.pop())
    for col in deck[4:]:
        for i in range(6):
            col.append(cards.pop())
    return deck

def main():
    currentCards = initCards(shuffle = True)

    for col in currentCards:
        print(f"[{' '.join(card.value for card in col)}]")

if __name__ == "__main__":
    main()
