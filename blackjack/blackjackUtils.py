import pandas as pd
import numpy as np
import seaborn as sns
import os
import datetime as dt
from numpy import random

def build_deck():
    numbers=list(range(2,15))
    suits = ['H','S','C','D']
    deck = []
    for i in numbers:
        for s in suits:
            card = s+str(i)
            deck.append(card)
    return deck

class Deck (object):
    def __init__ (self):
      self.deck = build_deck()
    
    def shuffle (self):
      random.shuffle (self.deck)
    
    def __len__ (self):
      return len (self.deck)
    
    def deal (self):
      if len(self) == 0:
        return None
      else:
        return self.deck.pop(0)
    
    def reconcile(self,listCards):
        self.deck = [a for a in self.deck if a not in listCards]
    
    def dealNumber(self,n):
        hand = [self.deal() for i in range(0,n)]
        return hand

def reformatInt(card):
    someInt = int(card[1:])
    if someInt == 14:
        return 11
    elif someInt >= 10:
        return 10
    else:
        return someInt

def score_hand(hand,convert=False):
    if convert:
        # this takes unformatted deck
        hand = [reformatInt(a) for a in hand]

    if 11 in hand and sum(hand) > 21:
        hand = [a if hand != 11 else 1 for a in hand]

    return sum(hand)

def dealerLogic(dealerHand,deck,convert=False):
    score = score_hand(dealerHand,convert)
    while score < 17:
        dealerHand += [reformatInt(deck.deal())]
        score = score_hand(dealerHand)

        if score > 21 and 11 in dealerHand:
            dealerHand = [a if a != 11 else 1 for a in dealerHand]
            score = score_hand(dealerHand)

    return dealerHand,score

def reformatHand(l):
    return [reformatInt(a) for a in l]

def playBlackjack(hardTable,softTable,splitTable,surrTable,bet=5,double=True,
        surrender=True,DAS=True,verbose=False,manualHand=None,manualDealer=None,blackjackPayout=3/2):
    # deal and set up deck
    deck = Deck()
    deck.shuffle()
    
    handRaw = deck.dealNumber(2)
    dealerHandRaw = deck.dealNumber(2)

    dealerHand = reformatHand(dealerHandRaw)
    hand = reformatHand(handRaw)

    if manualHand != None:
        hand = manualHand

    if manualDealer != None:
        dealerHand = manualDealer
    
    # dealer upcard is [0] of dealerHand variable
    dealerUp = dealerHand[0]

    if verbose:
        print('dealer raw hand: {}'.format(dealerHandRaw))
        print('dealer cards dealt: {}, dealer card faceup: {}'.format(dealerHand,dealerUp))

        print('player raw hand: {}'.format(handRaw))
        print('player dealt: {}'.format(hand))

    # check if surrender
    if surrender:
        if dealerUp in surrTable.columns:
            handScore = sum(hand)
            if handScore in surrTable.index:
                if surrTable[dealerUp].loc[handScore] == 'sur':
                    if verbose:
                        print('surrendering')
                    return bet*0.5

    # check if split
    if len(set(hand)) == 1 and len(hand) == 2:
        uPair = list(set(hand))[0]
        if splitTable[dealerUp].loc[uPair] == 'y':
            hands = [[hand[0],reformatInt(deck.deal())],[hand[1],reformatInt(deck.deal())]]
            if verbose:
                print('splitting cards')

    else:
        hands = [hand]

    endScores = []

    if verbose:
        print('all hands: {}'.format(hands))
    
    for hand in hands:
        subBet = bet
        someBool = True
        while someBool:

            if sum(hand) > 17:
                action = 's'
            
            # check if aces and should use softTable
            elif 11 in hand:
                if verbose:
                    print('using soft table as ace was found')
                scoreNoAce = sum([a for a in hand if a != 11])
                score = sum(hand)

                action = softTable[dealerUp].loc[scoreNoAce]

            else: # use hard table
                score = sum(hand)
                if verbose:
                    print('using hard table no ace')

                action = hardTable[dealerUp].loc[score]

            # process the action
            if action == 's': # stand
                print('stand')
                someBool = False
                score = sum(hand)
                endScores.append((score,bet))
                continue

            if double:

                # the difference between ds and d is what to do if double is not allowed (double=False)
                # if doubling is allowed, there is no difference since when you double you get another card and then stand
                if action == 'ds' or action == 'd':
                    someBool = False
                    print('doubled bet: {}'.format(subBet*2))
                    hand += [reformatInt(deck.deal())]
                    score = score_hand(hand)
                    endScores.append((score,subBet*2))
                    continue

                # if action == 'ds': # double and stand

                #     # bet *= 2
                #     someBool = False
                #     hand += reformatInt(deck.deal())
                #     score = score_hand(hand)
                #     endScores.append((score,subBet*2))
                #     print('doubled bet: {}'.format(subBet))
                #     continue

                # if action == 'd': # double and hit
                #     hand += reformatInt(deck.deal())
                #     score = score_hand(hand)
                #     subBet *= 2

                #     print('doubled bet: {}'.format(subBet))

            if not double:
                 
                if action == 'ds':
                    print('stand')
                    someBool = False
                    endScores.append((score,subBet))
                    continue

            # assume hit
            hand += [reformatInt(deck.deal())]
            print('hit, new hand: {}'.format(hand))

            score = score_hand(hand)
            if score > 21: # break
                print('broke')
                if 11 in hand:
                    if verbose:
                        print('broke but had ace so now treating like a 1')
                    hand = [a if a != 11 else 1 for a in hand]
                else:
                    someBool = False
                    endScores.append((score,subBet))

    # have dealer play 
    dealerFinalHand,dealerFinalScore = dealerLogic(dealerHand,deck)

    if verbose:
        print('final dealer hand: {}, final dealer score: {}'.format(dealerFinalHand,dealerFinalScore))

    # nonBustBets = [b for (s,b) in endScores if s <= 21]

    # check if push
    pushed = [(s,b) for (s,b) in endScores if s <= 21 and s == dealerFinalHand]

    # check if dealer broke
    if dealerFinalScore > 21:
        if verbose:
            print('dealer busted')
        winningBets = [(s,b) for (s,b) in endScores if s <= 21]

    else:
        winningBets = [(s,b) for (s,b) in endScores if s <= 21 and s > dealerFinalScore]

    if len(winningBets) == 0:
        loses = sum([-b for (s,b) in endScores])
        if verbose:
            print('no winnings, total losses: {}'.format(loses))
        return loses

    winnings = sum([b*2 if s != 21 else (b*blackjackPayout+b) for (s,b) in winningBets])
    if verbose:
        print('total winnings: {}'.format(winnings))

    return winnings




## create the strategy cards
# https://www.blackjackapprenticeship.com/blackjack-strategy-charts/
# columns are dealer hand, indexes are player hand, hard table is w/o aces, soft is w aces, DAS is double after splits

hardTable = pd.DataFrame({
    2: ['s','s','s','s','s','h','d','d','h','h'],
    3: ['s','s','s','s','s','h','d','d','d','h'],
    4: ['s','s','s','s','s','s','d','d','d','h'],
    5: ['s','s','s','s','s','s','d','d','d','h'],
    6: ['s','s','s','s','s','s','d','d','d','h'],
    7: ['s','h','h','h','h','h','d','d','h','h'],
    8: ['s','h','h','h','h','h','d','d','h','h'],
    9: ['s','h','h','h','h','h','d','d','h','h'],
    10: ['s','h','h','h','h','h','d','h','h','h'],
    11: ['s','h','h','h','h','h','d','h','h','h'],
},index=[a for a in range(8,18)][::-1])

softTable = pd.DataFrame({
    2: ['s','s','ds','h','h','h','h','h'],
    3: ['s','s','ds','d','h','h','h','h'],
    4: ['s','s','ds','d','d','d','h','h'],
    5: ['s','s','ds','d','d','d','d','d'],
    6: ['s','ds','ds','d','d','d','d','d'],
    7: ['s','s','s','h','h','h','h','h'],
    8: ['s','s','s','h','h','h','h','h'],
    9: ['s','s','h','h','h','h','h','h'],
    10: ['s','s','h','h','h','h','h','h'],
    11: ['s','s','h','h','h','h','h','h'],
},index=[a for a in range(2,10)][::-1])

splitTable = pd.DataFrame({
    2: ['y','n','y','y','y','yn','n','n','yn','yn'],
    3: ['y','n','y','y','y','y','n','n','yn','yn'],
    4: ['y','n','y','y','y','y','n','n','y','y'],
    5: ['y','n','y','y','y','y','n','yn','y','y'],
    6: ['y','n','y','y','y','y','n','yn','y','y'],
    7: ['y','n','n','y','y','n','n','n','y','y'],
    8: ['y','n','y','y','n','n','n','n','n','n'],
    9: ['y','n','y','y','n','n','n','n','n','n'],
    10: ['y','n','n','y','n','n','n','n','n','n'],
    11: ['y','n','n','y','n','n','n','n','n','n'],
},index=[a for a in range(2,12)][::-1])

surrTable = pd.DataFrame({
    9:['sur',0,0],
    10:['sur','sur',0],
    11:['sur',0,0],
},index=[16,15,14])


## testing and validation
# t = playBlackjack(hardTable,softTable,splitTable,surrTable,bet=5,verbose=True,manualHand=[9,9],manualDealer=[6,10])
# print('winnings: {}'.format(t))

# # splits
# t = playBlackjack(hardTable,softTable,splitTable,surrTable,bet=5,verbose=True,manualHand=[9,9],manualDealer=[6,10])
# print('winnings: {}'.format(t))

# # surrender
# t = playBlackjack(hardTable,softTable,splitTable,surrTable,bet=5,verbose=True,manualHand=[10,6],manualDealer=[9,10])
# print('winnings: {}'.format(t))

# # double and stand
# t = playBlackjack(hardTable,softTable,splitTable,surrTable,bet=5,verbose=True,manualHand=[11,7],manualDealer=[2,10])
# print('winnings: {}'.format(t))

# double and hit
t = playBlackjack(hardTable,softTable,splitTable,surrTable,bet=5,verbose=True,manualHand=[11,6],manualDealer=[3,10])
print('winnings: {}'.format(t))

print('complete')





