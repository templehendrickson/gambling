import numba
from numba import jit
import itertools

import os
import pandas as pd
import numpy as np
import time

import random

@jit(nopython=True)
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

def combinations(arr, n):
    arr = np.asarray(arr)
    t = np.dtype([('', arr.dtype)]*n)
    result = np.fromiter(itertools.combinations(arr, n), t)
    return result.view(arr.dtype).reshape(-1, n)

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

def score_hand(hand,scoreOnly=False):
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
            score = 135
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif dif == 4 and max(rnum) == 1:
            handtype = 'straight_flush'
            score = 120 + max(numbers)
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif 4 in rnum:
            handtype == 'four of a kind'
            score = check_four_of_a_kind(hand,letters,numbers,rnum,rlet)
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif sorted(rnum) == [2,2,3,3,3]:
            handtype == 'full house'
            score = check_full_house(hand,letters,numbers,rnum,rlet)
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif 3 in rnum:
            handtype = 'three of a kind'
            score = check_three_of_a_kind(hand,letters,numbers,rnum,rlet)
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif rnum.count(2) == 4:
            handtype = 'two pair'
            score = check_two_pair(hand,letters,numbers,rnum,rlet)
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        elif rnum.count(2) == 2:
            handtype = 'pair'
            score = check_pair(hand,letters,numbers,rnum,rlet)
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
        else:
            handtype = 'flush'
            score = 75 + max(numbers)/100
#             print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif 4 in rnum:
        handtype = 'four of a kind'
        score = check_four_of_a_kind(hand,letters,numbers,rnum,rlet)
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif sorted(rnum) == [2,2,3,3,3]:
       handtype = 'full house'
       score = check_full_house(hand,letters,numbers,rnum,rlet)
#        print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif 3 in rnum:
        handtype = 'three of a kind' 
        score = check_three_of_a_kind(hand,letters,numbers,rnum,rlet)
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 4:
        handtype = 'two pair'
        score = check_two_pair(hand,letters,numbers,rnum,rlet)
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif rnum.count(2) == 2:
        handtype = 'pair'
        score = check_pair(hand,letters,numbers,rnum,rlet)
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 
    elif dif == 4:
        handtype = 'straight'
        score = 65 + max(numbers)
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 

    else:
        handtype= 'high card'
        n = sorted(numbers,reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
#         print('this hand is a %s:, with score: %s' % (handtype,score)) 

    if scoreOnly:
        return score
        
    return score,handtype

def reconcileHands(cards,targ,deckObj):
    
    if len(cards) != 0:
        deckObj.reconcile(cards)
        
    numNeeded = targ - len(cards)
    
    newCards = deckObj.dealNumber(numNeeded)
    
    newHand = newCards + cards
    
    return newHand

def playGame(hand=[],flop=[],turn=[],river=[],numPlayers=6):
    # deck = np.array(build_deck())
    # randShuffle = uniqueRandIntsNb(len(deck),len(deck))
    
    deck = Deck()
    deck.shuffle()
    
    # iterate the defined hands
    
    hand = reconcileHands(hand,2,deck)
    flop = reconcileHands(flop,3,deck)
    turn = reconcileHands(turn,1,deck)
    river = reconcileHands(river,1,deck)
    
    # # initialize players
    # players = {}
    # if hand != []:
    #     players['p0'] = hand
        
    # else:
    #     players['p0'] = list(deck[randShuffle[0:2]])
    
    players = {}
    players['p0'] = hand
    
    # create other players
    for i in range(1,numPlayers):
        players['p{}'.format(i)] = deck.dealNumber(2)
        
    # # create other players
    # p1,p2 = 2,4
    # for i in range(1,numPlayers):
    #     players['p{}'.format(i)] = list(deck[p1:p2])
    #     p1 += 2
    #     p2 += 2
        
    # deal that flop,turn,river
    
    # if len(flop) != []:
    #     flop = list(deck[randShuffle[p2:p2+3]])
    # # flop = flop + list(deck[randShuffle[p2:p2]])
        

    # if turn == []:
    #     turn = [deck[randShuffle[p2+3]]]

    # if river == []:
    #     river = [deck[randShuffle[p2+4]]]

    allCards = flop + turn + river
    # get all combinators and score each player

    currWinner = ''
    currWinScore = 0
    for p in list(players.keys()):
        combos = combinations(players[p] + allCards, 5)
        scores = [score_hand(c,scoreOnly=True) for c in combos]
        if max(scores) > currWinScore:
            currWinScore = max(scores)
            currWinner += p

    if currWinner == 'p0':
        return 1
    
    return 0

## testing 

# o = playGame(hand=['D13','H13'])

def runSimulation(numSims,hand=[],flop=[],turn=[],river=[],numPlayers=6):
    
    res = np.array([playGame(hand,flop,turn,river,numPlayers) for i in range(0,numSims)])
    
    return res

def percentileOfScore(score,arr):
    res = (score-1) / (np.max(arr) - 1)
    return res

def computeProbability(hand,dealt):
    # compute the distribution of possible scores excluding those in hand and dealt

    deck = Deck()
    deck.shuffle()

    deck.reconcile(hand+dealt)

    # player best score
    playerCombos = combinations(hand+dealt,5)
    bestScore = max([score_hand(c,scoreOnly=True) for c in playerCombos])

    # compute all possible scores
    allCombos = combinations(deck.deck+dealt,5)
    scores = [score_hand(c,scoreOnly=True) for c in allCombos]

    # find percentile of player score against all possible
    playerPercentile = percentileOfScore(bestScore,np.array(scores))

    # probability of someone having better hand
    lossProb = (1-playerPercentile)

    return playerPercentile,lossProb

def percentFormat(a):
    return round(a*100,4)

# t1,t2 = computeProbability(['D13','H13'],['C13','H10','S10'])

# print('percentile of hand in possible outcomes: {}%, percent chance of loss: {}%'.format(percentFormat(t1),percentFormat(t2)))


    

# sims = runSimulation(1000,hand=['D13','H13'],flop=['C13'])

# print('probability of winning hand (n=1,000) w pocket kings and 1 kind in the flop: {}%'.format(round(np.sum(sims)/len(sims)*100,4)))
