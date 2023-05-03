import json
import sys
f = open(sys.argv[1],"r")
nfa=json.load(f)

def getTransitionState(x):
    mp={}
    for y in range(len(x)):
        lis=getlistOfTransitions(x[y])
        for j in lis:
            if j[0] not in mp:
                mp[j[0]]=[]
                temp = len(mp[j[0]])
                tempval = j[1]
                mp[j[0]].insert(temp,tempval)
            else:
                if j[1] not in mp[j[0]]:
                    temp = len(mp[j[0]])
                    tempval = j[1]
                    mp[j[0]].insert(temp,tempval)
    
    return mp


def getlistOfTransitions(xt):
    listt=[]
    global nfa
    
    for k in nfa["Transition Function"]:
        if k[0] == xt:
            temp = len(listt)
            templist = [k[1],k[2]]
            listt.insert(temp,templist)
    return listt


dfa={}
dfa["Alphabet"]=nfa["Alphabet"]
dfa["Start State"]=[]
for i in range(len(nfa["Start State"])):
    indx = len(dfa["Start State"])
    dfa["Start State"].insert(indx,[nfa["Start State"][i]])

dfa["States"]=[]
dfa["Transition Function"]=[]
dfa["Final State"]=[]

x=len(nfa["States"])
x=2**x
States=[]
for i in range(x):
    pstate=[]
    for j in range(len(nfa["States"])):
        if i & (2**j):
            temp = len(pstate)
            tempval = nfa["States"][j]
            pstate.insert(temp,tempval)
    temp = len(States)
    tempval = pstate
    States.insert(temp,tempval)

for x in States:
    if x == []:
        for t in nfa["Alphabet"]:
            temp = len(dfa["Transition Function"])
            tempval = [[],t,[]]
            dfa["Transition Function"].insert(temp,tempval)
        continue
    l=getTransitionState(x)
    for key in (l):
        temp = len(dfa["Transition Function"]) 
        l[key].sort(key=lambda x:int(x[1:len(x)]))
        # tempval = 
        dfa["Transition Function"].insert(temp,[x,key,l[key]])
    for key in nfa["Alphabet"]:
        if key not in l:
            temp = len(dfa["Transition Function"])
            tempval = [x,key,[]]
            dfa["Transition Function"].insert(temp,tempval)

dfa["States"]=States
finalStates=set({})

for x in nfa["Final State"]:
    for j in dfa["Transition Function"]:
        check1 = j[2]
        check2 = j[0]
        if x in check1:
            tempset = set({tuple(j[2])})
            finalStates.update(tempset)
        if x in check2:
            tempset = set({tuple(j[0])})
            finalStates.update(tempset)

finalStates=[list(x) for x in finalStates]
dfa["Final State"]=finalStates
g = open(sys.argv[2],'w')
json.dump(dfa,g,indent=6)