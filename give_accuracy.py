#Input the size of N (n) and return randomly drawn accuracy in (0.5,1).
#average_accuracy uses input of profile D and accuracy Q, and returns the average accuracy of all gurus, taking weight of gurus into consideration.

from random import seed
from random import gauss

def give_accuracy(n):
    accuracy=[]
    for _ in range(n):
        value=round((gauss(0,1)/8+0.75),3) #value is drawn by gaussian
        if value<0.5:           #distribution with mu=0 and var=1,
            value=0.5           #and the range of [mu-2var,mu+2var]
        if value>1:             #is taken and affine transformed to [0.5,1].
            value=1             #all value less than 0.5 is 0.5, more than 1 is
        accuracy.append(value)  #1.
    return accuracy             #return n-element vector of accuracy.
