import index
import numpy as np
from cal_banzhaf import cal_banzhaf
import math
from statistics import mean
import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns

plt.rcParams.update({'font.size': 16})
n=30
var_p=10
p=[i/10 for i in range(var_p)]
rp=50
beta=math.floor(n/2)+1
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
gini=[] #gini of DB
acu=[] #average accuracy
avgacu_trivial_p=0
D_bp=np.load('var_p_best_30n_50_10.npy')#read IBRD profiles
D_op=np.load('var_p_one_30n_50_10.npy')#read OSI profiles
Q_p=np.load('var_p_Q_30n.npy').item().get(0) #read accuracy
count=0
chain1=[]
chain2=[]
chain3=[]
ban1=[]
ban2=[]
ban3=[]
for i in range(var_p):#get statistics from profiles
    for j in range(rp):
        print('processing #',count,'/',var_p*rp*2)
        count=count+1
        d=D_bp.item().get(i*rp+j)
        r.append([p[i],'IBRD',index.del_r(d,n)])
        chain=index.chain(d,n)
        lon.append([p[i],'IBRD',chain[0]])
        short.append([p[i],'IBRD',chain[1]])
        avglen.append([p[i],'IBRD',chain[2]])
        for k in range(n):
            ban.append(cal_banzhaf(d,n,k,beta))
        ban_s=index.banzhaf(ban,n)
        ma.append([p[i],'IBRD',ban_s[0]])
        mi.append([p[i],'IBRD',ban_s[1]])
        avgban.append([p[i],'IBRD',ban_s[2]])
        gini.append([p[i],'IBRD',index.gini(ban,n)])
        acu.append([p[i],'IBRD',index.average_accuracy(d,Q_p,n)])
        ban=[]
    for j in range(rp):
        print('processing #',count,'/',var_p*rp*2)
        count=count+1
        d=D_op.item().get(i*rp+j)
        r.append([p[i],'OSI',index.del_r(d,n)])
        chain=index.chain(d,n)
        lon.append([p[i],'OSI',chain[0]])
        short.append([p[i],'OSI',chain[1]])
        avglen.append([p[i],'OSI',chain[2]])
        for k in range(n):
            ban.append(cal_banzhaf(d,n,k,beta))
        ban_s=index.banzhaf(ban,n)
        ma.append([p[i],'OSI',ban_s[0]])
        mi.append([p[i],'OSI',ban_s[1]])
        avgban.append([p[i],'OSI',ban_s[2]])
        gini.append([p[i],'OSI',index.gini(ban,n)])
        acu.append([p[i],'OSI',index.average_accuracy(d,Q_p,n)])
        ban=[]
fr=DataFrame(r,columns=['p','dynamics','value'])#generate pandas table of the above statistics
flong=DataFrame(lon,columns=['p','dy','value'])
fshort=DataFrame(short,columns=['p','dy','value'])
favglen=DataFrame(avglen,columns=['p','dy','value'])
fmax=DataFrame(ma,columns=['p','dynamics','value'])
fmin=DataFrame(mi,columns=['p','dynamics','value'])
favgban=DataFrame(avgban,columns=['p','dynamics','value'])
fgini=DataFrame(gini,columns=['p','dynamics','value'])
facu=DataFrame(acu,columns=['p','dynamics','value'])

qp=[mean(Q_p) for _ in range(var_p)]
plt.figure(1,figsize=(24,15)) #generate bar plots for the above statistics
sns.catplot(x='p',y='value',hue='dynamics',kind='bar',data=fr)
plt.xlabel('p')
plt.ylabel('mean ratio of delegators')
plt.savefig('ar_var_p_30n_50times_bar.pdf')
plt.figure(2,figsize=(24,15))
sns.catplot(x='p',y='value',hue='dy',kind='bar',data=flong)
plt.xlabel('p')
plt.ylabel('average longest chain')
plt.savefig('long_var_p_30n_50times_bar.pdf')
plt.figure(3,figsize=(24,15))
sns.catplot(x='p',y='value',hue='dy',kind='bar',data=fshort)
plt.xlabel('p')
plt.ylabel('average shortest chain')
plt.savefig('short_var_p_30n_50times_bar.pdf')
plt.figure(4,figsize=(24,15))
sns.catplot(x='p',y='value',hue='dy',kind='bar',data=favglen)
plt.xlabel('p')
plt.ylabel('average longth of chains')
plt.savefig('avglength_var_p_30n_50times_bar.pdf')
plt.figure(5,figsize=(24,15))
sns.catplot(x='p',y='value',hue='dynamics',kind='bar',data=fmax)
plt.xlabel('p')
plt.ylabel('mean maximum Banzhaf index')
plt.savefig('maxban_var_p_30n_50times_bar.pdf')
plt.figure(6,figsize=(24,15))
sns.catplot(x='p',y='value',hue='dynamics',kind='bar',data=fmin)
plt.xlabel('p')
plt.ylabel('mean minimum Banzhaf index')
plt.savefig('minban_var_p_30n_50times_bar.pdf')
plt.figure(7,figsize=(24,15))
sns.catplot(x='p',y='value',hue='dynamics',kind='bar',data=favgban)
plt.xlabel('p')
plt.ylabel('mean average Banzhaf index')
plt.savefig('avgban_var_p_30n_50times_bar.pdf')
plt.figure(8,figsize=(24,15))
sns.catplot(x='p',y='value',hue='dynamics',kind='bar',data=fgini)
plt.xlabel('p')
plt.ylabel('mean Gini coefficient')
plt.savefig('gini_var_p_30n_50times_bar.pdf')
plt.figure(9,figsize=(24,15))
sns.catplot(x='p',y='value',hue='dynamics',kind='bar',data=facu)
plt.plot(p,qp,label='trivial')
plt.xlabel('p')
plt.ylabel('mean average accuracy')
plt.savefig('acu_var_p_30n_50times_bar.pdf')

