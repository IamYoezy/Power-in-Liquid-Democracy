import generate_graph
import give_accuracy
import delegate
import math
import numpy as np
import cal_banzhaf
import index

n=30
A=[0,0.25,0.5,0.75,1] #values of A
beta=math.floor(n/2)+1 #quota
p=0.75 #p of random network
ra=0
rp=50
count=0
dele=[]
pro_best={}
pro_one={}
Q_final={}
Q=give_accuracy.give_accuracy(n) #randomly generate accuracy
while ra<=0.05: #choose an accuracy, with which at least 5% agents want to delegate.
    Q=give_accuracy.give_accuracy(n)
    [B,G]=generate_graph.draw_random(n,0.75) 
    D=delegate.best_response_delegation(n,G,Q,beta,dele,1)
    ra=index.del_r(D,n)
Q_final[0]=Q
np.save('var_beta_Q_30n.npy',Q_final) #save accuracy
print("Q is determined!")
for i in A:
    r=[]
    for _ in range(rp):
        print("processing #",count,"of",rp*len(A))
        [B,G]=generate_graph.draw_random(n,p) #generate random network
        D_best=delegate.best_response_delegation(n,G,Q,beta,dele,i) #return IBRD profile
        D_one=delegate.one_shot_delegation(n,G,Q,beta,i) #return OSI profile
        pro_best[count]=D_best
        pro_one[count]=D_one
        count=count+1
        np.save('var_A_best_30n_50_10.npy',pro_best) #save IBRD profiles
        np.save('var_A_one_30n_50_10.npy',pro_one)   #save OSI profiles
