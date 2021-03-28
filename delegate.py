#Generate delegation profile in three ways: random, best response dynamics, and one shot game.
#For random, input the size of agents (n), and return a delegation profile.
#For best response dynamics and one shot game, input the size of agents n, underlying network G, and the list of accuracy q, and return a delegation profile.
import random
import generate_graph
import give_accuracy
from cal_banzhaf import cal_banzhaf
from guru_of import guru_of
import numpy as np
import math


def trivial(n):
    D={}
    for i in range(n):
        D[i]={i:{}}
    return D #input n and output trivial profile

def random_delegate(n):
    N=[i for i in range(n)]
    D={}
    DR={}
    for i in range(n):
        D[i]={i:{}}
        DR[i]=i
    for i in range(n):
        de=random.choice(N)
        DR[i]=de
        guru=guru_of(DR,i,n)
        while guru=="cycle":
            de=random.choice(N)
            DR[i]=de
            guru=guru_of(DR,i,n)
        D[i].pop(i)
        D[de][i]={}
    for i in range(n):
        if D[i]=={}:
            D.pop(i)
    return D #return random profile in complete network


def give_epsilon(n,beta):
    rp=5
    size=20
    var=[]
    expectation=[]
    ratio=[]
    N=[i for i in range(n)]
    for _ in range(rp):
        banzhaf=[]
        Q=give_accuracy.give_accuracy(n)
        D=random_delegate(n)
        sample=random.choice(N)
#        print("sample is:",sample)
        for _ in range(size):
            b=cal_banzhaf(D,n,sample,beta)
            banzhaf.append(b)
        a=np.array(banzhaf)
        ex=np.mean(a)
        var_1=np.var(a,ddof=1)
        var.append(var_1)
        expectation.append(ex)
    e=np.array(var)
    re=np.mean(e)
    return re #return epsilon, which is the mean of var, used as approximation.

def power(D,n,i,beta,A):
    if A==0:
        return 1
    else:
        a=cal_banzhaf(D,n,i,beta)
        if a==0:
            return a
        else:
            return a**A #return the power, which is DB^A

def best_response_delegation(n,G,Q,beta,dele,A): #if A=1, return DB.
    N=[i for i in range(n)]
    D={}   #dict of profile, and each element denotes agents directly delegating to the agent.
    for i in range(n):
        D[i]={i:{}}
    DR={}
    for i in D:
        DR[i]=i
    for i in dele:
        DR[i]=dele[i]
        D[dele[i]][i]={}
    signal="true"
    p=0
    q_e=np.mean(Q)
    while signal=="true":
        print("loop=",p)
        p=p+1
        signal="false"
        for i in range(n):
            print(i)
            if i in dele:
                continue
            origin=DR[i]
            u_before=Q[guru_of(DR,i,n)]*power(D,n,i,beta,A)
            target=random.choice(generate_graph.neighbor_of(G,D,i))
            D[DR[i]].pop(i)   #construct new
            D[target][i]={}   #profile
            DR[i]=target      #with chosen trustee
            guru=guru_of(DR,i,n)
            while guru=="cycle": #if the agent is caught in a cycle, choose again
                target=random.choice(generate_graph.neighbor_of(G,D,i))
                D[DR[i]].pop(i)
                D[target][i]={}
                DR[i]=target
                guru=guru_of(DR,i,n)
            u_after=Q[guru]*power(D,n,i,beta,A)
            repeat=1
            while u_after<=u_before and repeat<=len(G[i]): #choose a better trustee
                target=random.choice(generate_graph.neighbor_of(G,D,i))
                D[DR[i]].pop(i)
                D[target][i]={}
                DR[i]=target
                guru=guru_of(DR,i,n)
                while guru=="cycle":
                    target=random.choice(generate_graph.neighbor_of(G,D,i))
                    D[DR[i]].pop(i)
                    D[target][i]={}
                    DR[i]=target
                    guru=guru_of(DR,i,n)
                u_after=Q[guru]*power(D,n,i,beta,A)
                repeat=repeat+1
            if repeat>len(G[i]): #if cannot enhance utility after randomly choosing 
                D[DR[i]].pop(i)  #times of neighbors
                D[origin][i]={}  #do not change of type 1
                DR[i]=origin
                print("not1")
            elif origin==DR[i]:  #if choose herself
                print("not2")    #do not change of type 2
            else:
                signal="true"    #if some agent changes, this is ture and next round
        if p>50:                 #if more than 50 rounds, stop
            signal="false"       #mark in D[30] it did not converge
            D[30]={}
        print("profile is:",D)
    return D

def one_shot_delegation(n,G,Q,beta,A):
    D={}
    if beta==1:
        for i in range(n):
            D[i]={i:{}}
        return D
    else:
        p_before=(math.factorial(n-1)/(math.factorial(n-beta)*math.factorial(beta-1)))/2**(n-1)
        p_after=(math.factorial(n-2)/(math.factorial(n-beta)*math.factorial(beta-2)))/2**(n-1)
        for i in range(n):
            D[i]={}
        for i in G: #choose the best neighbor
            q=Q[i]*(p_before**A)
            target=i
            for j in G[i]:
                if Q[j]*(p_after**A)>q:
                    q=Q[j]*(p_after**A)
                    target=j
            D[target][i]={}
        for i in range(n):
            if D[i]=={}:
                D.pop(i)
        return D #return one-shot profile

def delegation_completenet(n,Q,beta):
    max=0
    target=0
    D={}
    N={}
    pop=[]
    for i in range(n):
        if Q[i]>max:
            max=Q[i]
            target=i
        D[i]={i:{}}
        N[i]={}
    signal="true"
    N.pop(target)
    run=0
    while signal=="true":
        run=run+1
        print("processing #:",run)
        signal="false"
        for i in pop:
            N.pop(i)
        pop=[]
        for i in N:
            print("agent:",i)
            banzhaf_bf=cal_banzhaf(D,n,i,beta)
            D[target][i]={}
            D.pop(i)
            banzhaf_af=cal_banzhaf(D,n,i,beta)
            if banzhaf_af*Q[target]>banzhaf_bf*Q[i]:
                pop.append(i)
                signal="true"
            elif banzhaf_af*Q[target]<=banzhaf_bf*Q[i]:
                D[target].pop(i)
                D[i]={i:{}}
    return len(N) #return the number of delegators of NE in complete network.

