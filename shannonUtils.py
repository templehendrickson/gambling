import numpy as np
import pandas as pd
import datetime as dt
import os

def randomWalk(curr,moveUp,moveDown):
    randNum = np.random.randint(0,2)
    
    if randNum == 1: # move up
        return curr + (curr * moveUp)
    
    if randNum == 0: # move down
        return curr - (curr * moveDown)

def initModel(n,moveUp,moveDown):
    res = [1]
    currN = 0
    
    while currN < n:
        o = randomWalk(res[-1],moveUp,moveDown)
        res.append(o)
        currN += 1
        
#         print(currN)
        
    return np.array(res)

def investmentModelCash(alloc,arr):
    
    cash = 50
    shares = 50
    
    cashArr = []
    sharesArr = []
    totalVal = []
    
    for p in arr:
        
        mv = shares * p
        
        currPortVal = mv + cash
        
        diffTarg = mv - alloc * currPortVal
        
        shares += -diffTarg / p
        
        cash += diffTarg
        
        totalVal.append(currPortVal)
        cashArr.append(cash)
        sharesArr.append(shares)

    # df formatting
    df = pd.DataFrame({'totalVal':totalVal,'cash':cashArr,'shares':sharesArr,'randomWalk':arr})
        
    return df

# resArr = initModel(50,1,0.5)

# t = investmentModelCash(0.5,resArr)

 