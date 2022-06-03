from operator import truediv
import sys
from unittest import skip

pTable = []
tTable = []
mIndex = 0
end = None
l1 = []
l2 = []
l3 = []
l4 = []

def fileParse(file):
	pTable = []
	tTable = []
	transition = []	
	i = []
	o = []
	file = open(file)
	for line in file:
		text = line.rstrip()
		if 'place' in text:
			print(text)
			pTable.append(text)
		if 'trans' in text:
			trans = line[:-1].split('~')
			i = file.readline().rstrip()[:-1]
			o = file.readline().rstrip()[:-1]
			print('in place')
			print(i[3:])
			tTable.append([trans[0], trans[1], i[3:], o[3:]])
	return pTable, tTable

def liveLevelCheck(trans):
	if len(trans[2])==1 and len(trans[3])==1:
		l1.append(trans[0])
	if len(trans[2])>1 and len(trans[3])==1:
		l2.append(trans[0])
	if len(trans[2])==1 and len(trans[3])>1:
		l3.append(trans[0])

def l4Check(trans, path):
	if trans[0] in l3:
		return

	if trans[0] in path:
		return

	path.append(trans)
	if trans[0] not in l1:
		return
	else:
		for t in tTable:
			if trans[0] == t[2]:
				l4Check(t)
		l1.remove(trans[0])
		l4.append(trans[0])


def dfsAnalysis(curr, visited):
	if curr == None:
		return 
	if curr[0] in visited:
		#l4Check(curr, visited)
		return


	global mIndex
	print('curr:')
	print(curr)
	transitions = []
	for trans in tTable:
		if trans[2] in curr:
			transitions.append(trans)
	print('transition to curr')
	print(transitions)
	if len(transitions)>1:
		if transitions[0][3] != transitions[1][3]:
			for t in transitions:
				print('M'+str(mIndex)+'    '+t[2]+'  '+t[3]+'  '+t[0]+'M'+str((mIndex+1)), end='')
				print()
				dfsAnalysis(t[3])
		else:
			print('M'+str(mIndex)+'    '+curr[2]+'  '+curr[3]+'  '+t[0][0]+','+t[1][0]+'M'+str((mIndex+1)), end='')
			print()
			dfsAnalysis(t[3])

	
	for o in curr[3]:
		print('M'+str(mIndex)+'->M'+str((mIndex+1)),end=',')
		mIndex+=1
	'''
	liveLevelCheck(curr)
	for o in curr[3]:
		for t in tTable:
			if o == tTable[2]:
				dfsAnalysis(t, visited)
			else:
				global end
				end = curr[0]
				return
	'''	
def boundnessCheck():
	if len(l3)>0 or len(l4)>0:
		return 'false'
	return 'true'

def safeCheck(bounded):
	if bounded:
		return True
	return False

def livenessCheck():
	liveness = 'False'
	if len(l3)>0:
		liveness =  'livelock'
	if len(l4)>0:
		liveness = 'quasi-live'
	if len(l4)==len(tTable):
		liveness = 'live'
	return liveness

def reachabilityAnalysis(file):
	global pTable, tTable
	pTable, tTable = fileParse(file)

	print('p table:')
	print(pTable)

	print('t table:')
	print(tTable)
	
	for t in tTable:
		print(t[0]+' ... '+t[1])

	print('M    P1  P2  Transition')
	curr = pTable[0]
	trans = tTable[0]

	dfsAnalysis(curr, [])

	boundness = boundnessCheck()
	liveness = livenessCheck()
	safe = safeCheck(boundness)


def main(file):
	reachabilityAnalysis(file)

if __name__ == "__main__":
	file = sys.argv[1]
	main(file)
