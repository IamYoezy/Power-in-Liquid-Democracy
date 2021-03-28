import generate_graph
import give_accuracy
import delegate
import math
import matplotlib.pyplot as plt
import numpy as np
import index
import cal_banzhaf

n=30 #agent number
times=10 #how many p to run
A=1 #A power of DB
avg_r=[]
rp=50
beta=math.floor(n/2)+1 #beta
count=0
ra=0 #temp ratio
dele=[]
pro_best={}
pro_one={}
Q_final={}
while ra<=0.05: #generate accuracy, with which at least 5% agents want to delegate
    Q=give_accuracy.give_accuracy(n)
    [B,G]=generate_graph.draw_random(n,0.7)
    D=delegate.best_response_delegation(n,G,Q,beta,dele,A)
    ra=index.del_r(D,n)
print("Q is determined!")
Q_final[0]=Q
for i in range(times):
    p=i/times
    r=[]
    for _ in range(rp):
        print("processing #",count,"of",times*rp)
        [B,G]=generate_graph.draw_random(n,p) #generate random network
        D_best=delegate.best_response_delegation(n,G,Q,beta,dele,A) #return IBRD profile
        D_one=delegate.one_shot_delegation(n,G,Q,beta,A) #return OSI profile
        pro_best[count]=D_best
        pro_one[count]=D_one
        count=count+1
np.save('var_p_best_30n_50_10.npy',pro_best) #save IBRD profiles
np.save('var_p_one_30n_50_10.npy',pro_one) #save OSI profiles
np.save('var_p_Q_30n.npy',Q_final) #save accuracy
