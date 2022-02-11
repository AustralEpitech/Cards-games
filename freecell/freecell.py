#!/usr/bin/env python3
import random

numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K'];
colors = ['H', 'C', 'D', 'S'];

class Card:
    def __init__(self, number: str, col: str):
        if not number in numbers or not col in colors:
            return none
        self.value = number + col

def initCards() -> list[Card]:
    cards = [Card(nb, col) for col in colors for nb in numbers]
    deck = [[] for i in range(8)]

    random.shuffle(cards)
    for col in deck[:4]:
        for i in range(7):
            col.append(cards.pop())
    for col in deck[4:]:
        for i in range(6):
            col.append(cards.pop())
    return deck

def main():
    currentCards = initCards()
    for col in currentCards:
        for card in col:
            print(card.value)

if __name__ == "__main__":
    main()
