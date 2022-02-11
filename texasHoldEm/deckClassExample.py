from dataclasses import dataclass
from typing import List,Optional,Any
import numpy as np

def build_deck():
    numbers=list(range(2,15))
    suits = ['H','S','C','D']
    deck = []
    for i in numbers:
        for s in suits:
            card = s+str(i)
            deck.append(card)
    return deck

@dataclass
class Deck:

    def __post_init__(self):

        self.deck = build_deck()

        self.shuffle()

    @staticmethod
    def build_deck() -> List[str]:
        numbers=list(range(2,15))
        suits = ['H','S','C','D']
        deck = []
        for i in numbers:
            for s in suits:
                card = s+str(i)
                deck.append(card)
        return deck
    
    def shuffle (self):
      np.random.shuffle(self.deck)
    
    def reconcile(self,listCards: List[str]):
        self.deck = [a for a in self.deck if a not in listCards]

    def deal(self,n: int) -> List[str]:

        cards = self.deck[:n]

        self.deck = self.deck[n:]

        return cards

##testing

someDeck = Deck()

test = someDeck.deal(3)

print(test)

print('complete')