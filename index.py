import cal_banzhaf
import numpy as np
import powerlaw

def gini(A,n):#A is banzhaf vector
    up=0 #record the numerator
    for i in range(n):
        for j in range(n):
            num=abs(A[i]-A[j])
            up=up+num
    mean=np.mean(A)
    bottom=2*n*n*mean
    return up/bottom #return the gini of vector A

def chain(D,n):
    for i in range(n):
        if i in D:
            continue
        else:
            D[i]={}
    guru={0:{}}
    longest=0
    shortest=n
    avg=0
    path=0 #number of paths
    length=[] #record the length of each path
    for i in D:
        if i in D[i]:
            guru[0][i]={}
    guru[1]={}
    for i in guru[0]:
        if len(D[i])==1:
            length.append(0) 
        for j in D[i]:
            if j!=i:
                guru[1][j]={}
    sign="true"
    if guru[1]=={}:
        sign="false"
    le=1
    while sign=="true": #list agents in the le-th level of each delegation tree
        guru[le+1]={}   #in guru[le]
        for i in guru[le]:
            if i in D and D[i]=={}:
                length.append(le)
                continue
            elif i in D and len(D[i])!=0:
                for j in D[i]:
                    guru[le+1][j]={}
        if guru[le+1]=={}:
            sign="false"
        else:
            le=le+1
    for i in length:
        path=path+1
        if i<shortest:
            shortest=i
        if i>longest:
            longest=i
        avg=avg+i
    if path==0:
        return longest,shortest,0
    else:
        avg=avg/path
        return longest,shortest,avg #return the longest/shortest/average length

def banzhaf(A,n):
    ma=0
    mi=1
    su=0
    for i in A:
        if i>ma:
            ma=i
        if i<mi:
            mi=i
        su=su+i
    return ma,mi,su/n #return the maximum/minimum/average element of A.

def del_r(D,n): #the ratio of delegating agents
    num=0
    for i in range(n):
        if i in D:
            if D[i]=={}:
                num=num+1
        else:
            num=num+1
    return num/n

def average_accuracy(D,Q,n):
    accuracy=0
    guru=[]
    weight={}
    for i in D:
        if i in D[i]: #list all gurus
            guru.append(i)
            D[i].pop(i)
    for i in guru: #count the collected delegations of each agent
        temp=[i]
        for k in temp:
            if k in D:
                for j in D[k]:
                    temp.append(j)    
        weight[i]=len(temp)
    for i in guru:
        accuracy=accuracy+Q[i]*weight[i]
    return accuracy/n #return the weighted average accuracy of all gurus

def power(D,n):
    num=[] #record the delegation number of agents
    guru={0:{}} #temp dict to count delegation number
    count=0 #temp var to count delegation number
    for i in range(n):
        if i in D:
            continue
        else:
            D[i]={}
    for i in D: #count the each agent's collected delegations
        if len(D[i])>0:
            if i in D[i]:
                count=1
            for j in D[i]:
                if j!=i:
                    guru[0][j]={}
            l=0
            while len(guru[l])!=0:
                for j in guru[l]:
                    count=count+1
                    guru[l+1]={}
                    if len(D[j])>0:
                        for k in D[j]:
                            guru[l+1][k]={}
                l=l+1
        num.append(count)
        count=0
        guru={0:{}}
    signal='true'
    for i in num:
        if i!=1:
            signal='false'
    if signal=='true':
        return 0 #if no delegation, return 0
    else:
        result=powerlaw.Fit(num)
        return result.power_law.alpha #return the exponent of power law
