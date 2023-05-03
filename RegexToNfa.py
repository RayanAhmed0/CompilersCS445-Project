import json
import numpy as np 
import sys

# here we initialize the number of states 
States=0


def get_pre(ch):
	if ch in ['+']:
		return 1
	if ch in ['*']:
		return 2
	if ch in ['.']:
		return 3
	if ch in ['(']:
		return 4
# this method will take the parsed input from the pars_str method 
def shunt(x):
	stack=[]
	outstring=""
	for i in x:
		ch=i
		if checkformat(ord(ch)):
			outstring=outstring+ch
		elif ch == '(':
			stack.insert(len(stack),ch)
		elif ch == ')':
			while len(stack)>0 and stack[len(stack)-1]!='(':
				outstring=outstring+stack[len(stack)-1]
				stack.pop(len(stack)-1)
			stack.pop(len(stack)-1)
		else:
			while len(stack)>0 and get_pre(ch)>=get_pre(stack[len(stack)-1]):
				outstring=outstring+stack[len(stack)-1]
				stack.pop(len(stack)-1)
			stack.insert(len(stack),ch)
	while len(stack)>0:
		outstring=outstring+stack[len(stack)-1]
		stack.pop(len(stack)-1)
	return outstring

def pars_str(x):
	res=[]
	for i in range(len(x)-1):
		res.insert(len(res),x[i])
		if checkformat(ord(x[i])) and checkformat(ord(x[i+1])):
			res.insert(len(res),'.')
		elif x[i]==')' and x[i+1] == '(':
			res.insert(len(res),'.')
		elif checkformat(ord(x[i+1])) and x[i]==')':
			res.insert(len(res),'.')
		elif x[i+1]=='(' and checkformat(ord(x[i])):
			res.insert(len(res),'.')
		elif x[i] == '*' and (checkformat(ord(x[i+1]) or x[i+1] == '(')):
			res.insert(len(res),'.')
	check = x[len(x)-1]
	if( check != res[len(res)-1]):
		res += check
	return ''.join(res)

def NFA_sym(ch):
	global Alphabet
	Alphabet.update(set({ch}))
	global States
	val = ["Q{}".format(States),ch,"Q{}".format(States+1)]
	nfa["Transition Function"].insert(len(nfa["Transition Function"]),val)
	States=States+2
	ret = list(["Q{}".format(States-2),"Q{}".format(States-1)])
	return ret

def nfa_unio(nfa1,nfa2):
	global States
	val = ["Q{}".format(States),'$',nfa1[0]]
	nfa["Transition Function"].insert(len(nfa["Transition Function"]),val)
	val = ["Q{}".format(States),'$',nfa2[0]]
	nfa["Transition Function"].insert(len(nfa["Transition Function"]),val)
	val = [nfa1[1],'$',"Q{}".format(States+1)]
	nfa["Transition Function"].insert(len(nfa["Transition Function"]),val)
	val = [nfa2[1],'$',"Q{}".format(States+1)]
	nfa["Transition Function"].insert(len(nfa["Transition Function"]),val)
	States=States+2
	return ["Q{}".format(States-2),"Q{}".format(States-1)]

def loop(nfa1):
	global States
	val = [nfa1[1],'$',nfa1[0]]
	nfa["Transition Function"].insert(len(nfa["Transition Function"]),val)
	val = ["Q{}".format(States),'$',nfa1[0]]
	nfa["Transition Function"].insert(len(nfa["Transition Function"]),val)
	val = [nfa1[1],'$',"Q{}".format(States+1)]
	nfa["Transition Function"].insert(len(nfa["Transition Function"]),val)
	val = ["Q{}".format(States),'$',"Q{}".format(States+1)]
	nfa["Transition Function"].insert(len(nfa["Transition Function"]),val)
	States=States+2
	return ["Q{}".format(States-2),"Q{}".format(States-1)]

def concatenation(nfa1,nfa2):
	global States
	indx = len(nfa['Transition Function'])
	val = [nfa1[1],'$',nfa2[0]]
	nfa['Transition Function'].insert(indx,val)
	return [nfa1[0],nfa2[1]]	

def re2nfa(x):
	stack=list([])
	xt=""
	for i in x:
		if checkformat(ord(i)):
			stack.insert(len(stack),NFA_sym(i))
		elif i == '+':
			xt=nfa_unio(stack[len(stack)-2],stack[len(stack)-1])
			stack.pop(len(stack)-1)
			stack.pop(len(stack)-1)
			stack.insert(len(stack),xt)
		elif i == "*":
			xt=loop(stack[len(stack)-1])
			stack.pop(len(stack)-1)
			stack.insert(len(stack),xt)
		else:
			xt=concatenation(stack[len(stack)-2],stack[len(stack)-1])
			stack.pop(len(stack)-1)
			stack.pop(len(stack)-1)
			stack.insert(len(stack),xt)
	nfa["Start State"]=[xt[0]]
	nfa["Final State"]=[xt[1]]

# in this function it will check for the format 
def checkformat(y):
	if (y<48 or y>57) and (y<97 or y>122) and (y<65 or y>90):
		return False
	return True

Alphabet=set({})

f = open(sys.argv[1],"r")
x=json.load(f)
nfa={}
nfa["States"]=[]
nfa["Alphabet"]=[]
nfa["Transition Function"]=[]
x=x["RE"]
x=pars_str(x)
x=shunt(x)
re2nfa(x)

s=set({})
for x in range(len(nfa["Transition Function"])):
	s.update(set({nfa["Transition Function"][x][0]}))
	s.update(set({nfa["Transition Function"][x][2]}))

templis = list(Alphabet)
nfa["Alphabet"]=templis
s=list(s)
s.sort(key=lambda a:int(a[1:]))
nfa["States"]=s

g = open(sys.argv[2],'w')
json.dump(nfa,g,indent=6)