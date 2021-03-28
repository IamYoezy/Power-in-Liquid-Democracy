#Given a profile, to find the guru of any agent.
#Input a reverse profile, the size of agents,and an agent, and output the guru of that agent.

def guru_of(DR,a,n):
    guru=a
    i=0
    while DR[guru]!=guru and i<=n:
        guru=DR[guru]
        i=i+1
    if i<=n: #if a is caught in a cycle i>n
        return guru
    else:
        return 'cycle' #if a is caught in a cycle, return string 'cycle'
