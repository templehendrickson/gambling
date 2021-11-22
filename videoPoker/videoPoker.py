# import numba
# from numba import jit
import itertools
import copy
import os
import pandas as pd
import numpy as np
import time
from tqdm import tqdm

import random

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

def combinations(arr, n):
    arr = np.asarray(arr)
    t = np.dtype([('', arr.dtype)]*n)
    result = np.fromiter(itertools.combinations(arr, n), t)
    return result.view(arr.dtype).reshape(-1, n)

def uniqueRandIntsNb(uBound,count):
    res = []
    for a in range(0,count):
        i = np.random.randint(uBound)
        if i not in res:
            res.append(i)
        else:
            while i in res:
                i = np.random.randint(uBound)
            res.append(i)
            
    return res

def findAllCombos(someCards):
    res = [[]]
    for n in [a for a in range(1,6)]:
        raw = combinations(someCards,n)
        res += [list(a) for a in raw]
        
    return res

def check_four_of_a_kind(hand,letters,numbers,rnum,rlet):
    for i in numbers:
            if numbers.count(i) == 4:
                four = i
            elif numbers.count(i) == 1:
                card = i
    score = 105 + four + card/100
    return score

def check_full_house(hand,letters,numbers,rnum,rlet):
    for i in numbers:
        if numbers.count(i) == 3:
            full = i
        elif numbers.count(i) == 2:
            p = i
    score = 90 + full + p/100  
    return score

def check_three_of_a_kind(hand,letters,numbers,rnum,rlet):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i
        else: 
            cards.append(i)
    score = 45 + three + max(cards) + min(cards)/1000
    return score

def check_two_pair(hand,letters,numbers,rnum,rlet):
    pairs = []
    cards = []
    for i in numbers:
        if numbers.count(i) == 2:
            pairs.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards,reverse=True)
    score = 30 + max(pairs) + min(pairs)/100 + cards[0]/1000
    return score

def check_pair(hand,letters,numbers,rnum,rlet):    
    pair = []
    cards  = []
    for i in numbers:
        if numbers.count(i) == 2:
            pair.append(i)
        elif numbers.count(i) == 1:    
            cards.append(i)
            cards = sorted(cards,reverse=True)
    score = 15 + pair[0] + cards[0]/100 + cards[1]/1000 + cards[2]/10000
    return score

def check_better_than_jacks(hand,letters,numbers,rnum,rlet):
    # in jacks or better video poker (and most for that matter), your hand only counts if better than or equal to pair of jacks
    pairs = [i for i in numbers if numbers.count(i) == 2]
    
    if list(set(pairs))[0] >= 11:

        return True

    return False

def score_hand(hand,payTable,scoreOnly=False):
    letters = [hand[i][:1] for i in range(5)] # We get the suit for each card in the hand
    numbers = [int(hand[i][1:]) for i in range(5)]  # We get the number for each card in the hand
    rnum = [numbers.count(i) for i in numbers]  # We count repetitions for each number
    rlet = [letters.count(i) for i in letters]  # We count repetitions for each letter
    dif = max(numbers) - min(numbers) # The difference between the greater and smaller number in the hand
    handtype = ''
    score = 0
    if 5 in rlet:
        if numbers ==[14,13,12,11,10]:
            handtype = 'royal_flush'
            score = payTable['royal_flush']
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif dif == 4 and max(rnum) == 1:
            handtype = 'straight_flush'
            score = payTable['straight_flush']
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif 4 in rnum:
            handtype == 'four of a kind'
            # score = check_four_of_a_kind(hand,letters,numbers,rnum,rlet)
            score = payTable['four_of_a_kind']
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif sorted(rnum) == [2,2,3,3,3]:
            handtype == 'full house'
            # score = check_full_house(hand,letters,numbers,rnum,rlet)
            score = payTable['full_house']
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif 3 in rnum:
            handtype = 'three of a kind'
            # score = check_three_of_a_kind(hand,letters,numbers,rnum,rlet)
            score = payTable['three_of_a_kind']
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif rnum.count(2) == 4:
            handtype = 'two pair'
            # score = check_two_pair(hand,letters,numbers,rnum,rlet)
            score = payTable['two_pairs']
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif rnum.count(2) == 2:
            handtype = 'pair'
            # score = check_pair(hand,letters,numbers,rnum,rlet)
            if check_better_than_jacks(hand,letters,numbers,rnum,rlet):
                score = payTable['better_jack_pair']
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        else:
            handtype = 'flush'
            # score = 75 + max(numbers)/100
            score = payTable['flush']
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif 4 in rnum:
        handtype = 'four of a kind'
        # score = check_four_of_a_kind(hand,letters,numbers,rnum,rlet)
        score = payTable['four_of_a_kind']
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif sorted(rnum) == [2,2,3,3,3]:
        handtype = 'full house'
    #    score = check_full_house(hand,letters,numbers,rnum,rlet)
        score = payTable['full_house']
#        print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif 3 in rnum:
        handtype = 'three of a kind' 
        # score = check_three_of_a_kind(hand,letters,numbers,rnum,rlet)
        score = payTable['three_of_a_kind']
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 4:
        handtype = 'two pair'
        # score = check_two_pair(hand,letters,numbers,rnum,rlet)
        score = payTable['two_pairs']
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 2:
        handtype = 'pair'
        # score = check_pair(hand,letters,numbers,rnum,rlet)
        # check if better than jacks
        if check_better_than_jacks(hand,letters,numbers,rnum,rlet):
            score = payTable['better_jack_pair']
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif dif == 4:
        handtype = 'straight'
        # score = 65 + max(numbers)
        score = payTable['straight']
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 

#     else:
#         handtype= 'high card'
#         n = sorted(numbers,reverse=True)
#         score = n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
# #         print('this hand is a %s:, with score: %s' % (handtype,score)) 

    if scoreOnly:
        return score
        
    return score,handtype

def simulateGame(hand,deckObj,payTable):

    # clone deck and reshuffle (this is so that each game is different)
    deckClone = copy.deepcopy(deckObj)
    deckClone.shuffle()
    newCards = deckClone.dealNumber(5 - len(hand))

    newHand = hand + newCards

    # score
    score = score_hand(newHand,payTable,scoreOnly=True)

    return score

def runSimGames(n,hand,deckObj,payTable):

    scores = np.array([simulateGame(hand,deckObj,payTable) for n in range(n)])

    # return total profit of n games
    profit = np.sum(scores) - (len(scores)*5)

    return profit

def findBestHand(cards,payTable,n=1000):
    # create deck with dealt cards removed
    deck = Deck()
    deck.shuffle()
    deck.reconcile(cards)

    # compute all combinations of n 1-5 card hands to keep
    allCombos = findAllCombos(cards)

    # dict of all combos
    simDict = {i : runSimGames(n,c,deck,payTable) for i,c in enumerate(allCombos)}

    maxScore = max([s for (i,s) in simDict.items()])
    bestHandIx = [i for (i,s) in simDict.items() if s == maxScore][0]
    bestHand = allCombos[bestHandIx]

    return bestHand,maxScore

def playGame(payTable,bet=5,pickRandom=False):

    deck = Deck()
    deck.shuffle()

    # 5 random cards
    dealt = deck.dealNumber(5)

    if not pickRandom:

        # findbest ones to keep
        bestHand,score = findBestHand(dealt,payTable)

    if pickRandom:

        # determine rand number cards to keep
        numCount = np.random.randint(0,5)
        randPulls = uniqueRandIntsNb(5,numCount)
        bestHand = [dealt[i] for i in randPulls]

    ## play and bet
    newCards = deck.dealNumber(5-len(bestHand))

    newHand = bestHand + newCards

    winAmount = score_hand(newHand,payTable,scoreOnly=True)

    pnl = winAmount + -bet

    return pnl

def simulateNumberGames(numberSims,payTable,bet=5,pickRandom=False):

    sims = np.array([playGame(payTable,bet,pickRandom) for n in tqdm(range(numberSims))])

    return sims

payTable = {
    'royal_flush':4000,
    'straight_flush':250,
    'four_of_a_kind':125,
    'full_house':45,
    'flush':30,
    'straight':20,
    'three_of_a_kind':15,
    'two_pairs':10,
    'better_jack_pair':5
}

# t = findBestHand(['D12','H2','S12','C10','S13'],payTable)
# t = findBestHand(['D11','H4','S11','C7','S8'],payTable)
# t = findBestHand(['H10','H11','H12','H13','H13'],payTable)

# print(t)
# t = playGame(payTable,pickRandom=True)

# print('complete')