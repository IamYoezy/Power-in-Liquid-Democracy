#This package is used to calculate the Banzhaf index of an agent based on a prfoile.
#This an approximation using Monte Carlo.
#Input the dic of the delegation profile D, the size of agent set n, and the target agent a, and the quota beta.
# Output is the Banzhaf index of agent a.
from cal_weight import cal_weight
import numpy as np
import random
import math


def cal_banzhaf(D,n,a,beta):
    DM=np.zeros((n,n)) #delegation matrix: DM[i][j] is i delegates to j
    for i in D:         #From the given dic of profile,
        for k in D[i]:  #generate the matrix.
            DM[k][i]=1
    swing=0             #Count for swing times
    rp=15000              #number of sample coalitions
    N=[] #sample pool
#    N_sample=[i for i in range(n)]
    for i in range(n):  #
        N.append(i)
    N.pop(a) #sample pool should not contain agent a
    #run=1
    for _ in range(rp): #each agent has 50% to be sampled in C
        sample=[]
        for i in range(n):
            if i!=a:
                p=random.random()
                if p>=0.5:
                    sample.append(i)
        weight1=cal_weight(D,DM,sample) #weight of C
        sample.append(a)
        weight2=cal_weight(D,DM,sample) #weight of C\cup {a}
        if weight1<beta and weight2>=beta:
            swing=swing+1  #count swing
    return swing/rp #return ratio of swing

def standard_banzhaf(n,a,beta,W):
    swing=0             #Count for swing times
    rp=15000              #number of sample coalitions
    for _ in range(rp):
        sample=[]
        for i in range(n):
            if i!=a:
                p=random.random()
                if p>=0.5:
                    sample.append(i)
        weight1=cal_weight.standard_weight(sample,W) #weight of C
        sample.append(a)
        weight2=cal_weight.standard_weight(sample,W) #weight of C\cup {a}
        if weight1<beta and weight2>=beta:
            swing=swing+1  #count swing
    return swing/rp
