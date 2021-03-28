import index
import numpy as np
from cal_banzhaf import cal_banzhaf
import math
from statistics import mean
import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns

plt.rcParams.update({'font.size': 20})
n=30
beta=math.floor(n/2)+1
A=[0,0.25,0.5,0.75,1]
rp=50
r=[] #ratio
chain=[]
lon=[] #longest chain
short=[] #shortest chain
avglen=[] #average length of chains
ban=[]
ban_s=[] #statistics from ban
ma=[] #max DB
mi=[] #min DB
avgban=[] #average DB
gini=[]#gini of DBs
acu=[] #average accuracy
con=[] # number of converged instances
avgacu_trivial_b=0
D_bb=np.load('var_A_best_30n_50_10.npy') #read IBRD profiles
D_ob=np.load('var_A_one_30n_50_10.npy')  #read OSI profiles
Q_b=np.load('var_A_Q_30n.npy').item().get(0) #read accuracy
count=0
chain1=[]
chain2=[]
chain3=[]
ban1=[]
ban2=[]
ban3=[]
concon=0 #count non-converging cases
for i in range(len(A)): #get statistics from profiles
    for j in range(rp):
        print('processing #',count,'/',len(A)*rp*2)
        count=count+1
        d=D_bb.item().get(i*rp+j)
        if 30 in d:
            concon=concon+1
            continue
        r.append([A[i],'IBRD',index.del_r(d,n)])
        chain=index.chain(d,n)
        lon.append([A[i],'IBRD',chain[0]])
        short.append([A[i],'IBRD',chain[1]])
        avglen.append([A[i],'IBRD',chain[2]])
        for k in range(n):
            ban.append(cal_banzhaf(d,n,k,beta))
        ban_s=index.banzhaf(ban,n)
        ma.append([A[i],'IBRD',ban_s[0]])
        mi.append([A[i],'IBRD',ban_s[1]])
        avgban.append([A[i],'IBRD',ban_s[2]])
        gini.append([A[i],'IBRD',index.gini(ban,n)])
        acu.append([A[i],'IBRD',index.average_accuracy(d,Q_b,n)])
        ban=[]
    con.append([A[i],1,50-concon])
    concon=0
    for j in range(rp):
        print('processing #',count,'/',len(A)*rp*2)
        count=count+1
        d=D_ob.item().get(i*rp+j)
        if index.chain(d,n)==0:
            continue
        r.append([A[i],'OSI',index.del_r(d,n)])
        chain=index.chain(d,n)
        lon.append([A[i],'OSI',chain[0]])
        short.append([A[i],'OSI',chain[1]])
        avglen.append([A[i],'OSI',chain[2]])
        for k in range(n):
            ban.append(cal_banzhaf(d,n,k,beta))
        ban_s=index.banzhaf(ban,n)
        ma.append([A[i],'OSI',ban_s[0]])
        mi.append([A[i],'OSI',ban_s[1]])
        avgban.append([A[i],'OSI',ban_s[2]])
        gini.append([A[i],'OSI',index.gini(ban,n)])
        acu.append([A[i],'OSI',index.average_accuracy(d,Q_b,n)])
        ban=[]
fr=DataFrame(r,columns=['A','dynamics','value']) #generate pandas table of the above statistics
flong=DataFrame(lon,columns=['A','dynamics','value'])
fshort=DataFrame(short,columns=['A','dynamics','value'])
favglen=DataFrame(avglen,columns=['A','dynamics','value'])
fmax=DataFrame(ma,columns=['A','dynamics','value'])
fmin=DataFrame(mi,columns=['A','dynamics','value'])
favgban=DataFrame(avgban,columns=['A','dynamics','value'])
fgini=DataFrame(gini,columns=['A','dynamics','value'])
facu=DataFrame(acu,columns=['A','dynamics','value'])
fcon=DataFrame(con,columns=['A','B','value'])

N=A
qb=[mean(Q_b) for _ in range(len(A))]
plt.figure(1,figsize=(22,13)) #generate bar plot of the above statistics
sns.catplot(x='A',y='value',hue='dynamics',kind='bar',data=fr)
plt.xlabel('\u03B1')
plt.ylabel('mean ratio of delegators')
plt.savefig('ar_beta_30n_50_bar.pdf')
plt.figure(2,figsize=(22,13))
sns.catplot(x='A',y='value',hue='dy',kind='bar',data=flong)
plt.xlabel('\u03B1')
plt.ylabel('longest chain')
plt.savefig('long_beta_30n_50_bar.pdf')
plt.figure(3,figsize=(22,13))
sns.catplot(x='A',y='value',hue='dy',kind='bar',data=fshort)
plt.xlabel('\u03B1')
plt.ylabel('shortest chain')
plt.savefig('short_beta_30n_50_bar.pdf')
plt.figure(4,figsize=(22,13))
sns.catplot(x='A',y='value',hue='dy',kind='bar',data=favglen)
plt.xlabel('\u03B1')
plt.ylabel('average length of chains')
plt.savefig('avglength_beta_30n_50_bar.pdf')
plt.figure(5,figsize=(22,13))
sns.catplot(x='A',y='value',hue='dynamics',kind='bar',data=fmax)
plt.xlabel('\u03B1')
plt.ylabel('mean maximum Banzhaf index')
plt.savefig('maxban_beta_30n_50_bar.pdf')
plt.figure(6,figsize=(22,13))
sns.catplot(x='A',y='value',hue='dynamics',kind='bar',data=fmin)
plt.xlabel('\u03B1')
plt.ylabel('mean minimum Banzhaf index')
plt.savefig('minban_beta_30n_50_bar.pdf')
plt.figure(7,figsize=(22,13))
sns.catplot(x='A',y='value',hue='dynamics',kind='bar',data=favgban)
plt.xlabel('\u03B1')
plt.ylabel('mean average Banzhaf index')
plt.savefig('avgban_beta_30n_50_bar.pdf')
plt.figure(8,figsize=(22,13))
sns.catplot(x='A',y='value',hue='dynamics',kind='bar',data=fgini)
plt.xlabel('\u03B1')
plt.ylabel('mean Gini coefficient')
plt.savefig('gini_beta_30n_50_bar.pdf')
plt.figure(9,figsize=(22,13))
sns.catplot(x='A',y='value',hue='dynamics',kind='bar',data=facu)
plt.xlabel('\u03B1')
plt.ylabel('mean average accuracy')
plt.savefig('acu_beta_30n_50_bar.pdf')
plt.figure(10,figsize=(22,13))
sns.catplot(x='A',y='value',hue='B',kind='bar',legend=None,data=fcon)
plt.xlabel('\u03B1')
plt.ylabel('# of converged instances')
plt.savefig('con_beta_30n_50_bar.pdf')

