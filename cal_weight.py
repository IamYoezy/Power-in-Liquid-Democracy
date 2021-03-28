#Calculate the weight of a coalition.
#Input the dic and matrix of delegation profile (D & DM), and the dic of coalition (C).
#Output the weight w.

import numpy as np

def cal_weight(D,DM,C):
    guru=[] #set of gurus in C
    n=len(DM[0])
    CD={}
    for i in C:
        CD[i]={}
    for i in CD: 
        if DM[i][i]==1:
            guru.append(i)
    for i in guru: #if delegator and the chain are contained in C, put into guru
        if i in D:
            for j in D[i]:
                if j in guru:
                    continue
                if j in CD:
                    guru.append(j)
    #from all gurus, check whether agents directly delegating to the guru in C or not. If in C, add to guru and check agents directly delegating to her.

    return len(guru)

def standard_weight(C,W): #calculate the weight for standard banzhaf index
    weight=0
    for i in C:
        weight=weight+W[i]
    return weight
