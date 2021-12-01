import pandas as pd
import numpy as np
from tqdm import tqdm

## kelly for even money bet
def kellyBet(prob):
    f = prob - (100 - prob)
    return f

def playGame(prob):
    ri = np.random.randint(1,100)
    
    if ri < prob: # win
        return 1
    return -1

def runSimulation(mu,sigma,accurate=False,n=1000,startingCash=100,fFrac=1,compRandom=False):
    if not accurate: # generate normal distribution w sigma and mu
        samples = np.random.normal(mu,sigma,n)
        
    else:
        samples = np.array([mu for _ in range(n)])
                     
    f = kellyBet(mu)*fFrac
    
    res = [startingCash]
    
    for s in samples:
        if compRandom:
            f = np.random.randint(1,100)
        bet = startingCash * f/100
        startingCash += (bet * playGame(s))
        res.append(startingCash)
        
    return np.array(res)

def runAutoSims(sigmas,fFrac=1):
    pdf = pd.DataFrame({'{}_std'.format(s) : runSimulation(60,s) for s in sigmas})
    pdf['accurate'] = runSimulation(60,1,accurate=True)
    pdf['random'] = runSimulation(60,1,accurate=True,compRandom=True)
    
    return pdf

def metaSims(n=1000,sigmas=[1,2,3],fFrac=1):
    res = []
    for x in tqdm(range(n)):
        out = runAutoSims(sigmas,fFrac)
        ranks = (out.iloc[-1] / out.iloc[0] - 1).values.argsort().argsort()
        
        res.append(tuple(ranks))
        
    resDf = pd.DataFrame(res,columns=['1_std', '2_std', '3_std', 'accurate','random'])
    
    return resDf