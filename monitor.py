import random
import numpy as np
import sys
import xlsxwriter

def readFile(fileName):
	file = open(fileName, "r")
	#contains ref and the name of the states - draft
	state = dict() 
	#contains the transactions - draft
	trans = dict()
	#contains the transactions - final
	T = list()
	lambdaq = dict()
	#contains the states - final
	S = list()
	#contains all the combinations of the alphabet - Sigma*
	AP = list()
	#contains the alphabets - Sigma
	Sq = list()
	for line in file:
		first = line.find("\"")
		second = line.find("\"", first + 1)
		third = line.find("\"", second + 1)
		fourth = line.find("\"", third + 1)
		fifth = line.find("\"", fourth + 1)
		sixth = line.find("\"", fifth + 1)
		arrow = line.find("->", second + 1, third)
		label = line.find("label", fourth + 1)

		if((first < second) and (second < arrow) and (arrow < third) and (third < fourth) and (fourth < label) and (label < fifth) and (fifth < sixth)):
			stateFrom = line[first + 1:second]
			stateTo = line[third + 1:fourth]
			s = line[fifth + 2:sixth - 1]
			if(not(stateFrom in state)):
				state[stateFrom] = 'q' + str(len(state))
			if(not(stateTo in state)):
				state[stateTo] = 'q' + str(len(state))
			trans[str(len(trans))] = {'from':state[stateFrom], 'to':state[stateTo], 's':s}

		label = line.find("label", second)
		style = line.find("style", label)
		color = line.find("color", style)

		if((label < style) and (style < color)):
			st = line[first + 1:second]
			if(st == "(0, 0)"):
				start = state[st]
			colour = line[color + 6:len(line) - 2]
			if(colour == "green"):
				lambdaq[state[st]] = 'T'
			elif(colour == "yellow"):
				lambdaq[state[st]] = '?'
			else:
				lambdaq[state[st]] = 'F'

	for key, val in state.items():
		S.append(val )

	for st1 in S:
		for st2 in S:
			tr = []
			for key, val in trans.items():
				if(val['from'] == st1 and val['to'] == st2):
					a = val['s'].replace('&&','')
					if(a == '<empty>'):
						a = ''
					tr.append(a)
					if(not(a in AP)):
						AP.append(a)
			T.append({'from': st1, 'to': st2, 's': tr})
	for a in AP:
		for b in a:
			if(not(b in Sq)):
				Sq.append(b)

	return S, T, AP, Sq, lambdaq, start

def readTrace(fileName):
	trace = list()
	file = open(fileName, 'r')

	for line in file:
		trace.append(line)
	return trace

def intersection(list1, list2): 
    return list(set(list1) & set(list2))

def main(numMonitors, fileName, kCrash, kRound, readDist, p):
	numMsg = 0;
	msgSize = 0;
	numRnds = 0;
	#crashArr = [0] * 100

	states, transitions, S, AP, lambdaq, start = readFile(fileName)
	trace = readTrace("trace.txt")
	QcurrentNextAll = [None] * numMonitors
	QcurrentAll = [start] * numMonitors
	numCrash = 0

	numComm = 0
	parView = [[dict()] * numMonitors] * kRound
	pos = 0
	for ti in trace:
		numComm = numComm + 1
		num2 = [''] * len(AP)

		#parView for each monitor
		#uniform distribution
		if(readDist == "uniform"):
			for a in range(0, len(AP)):
				num1 = random.randint(1, numMonitors - 1)
				num2[a] = random.sample(range(0, numMonitors), num1)
			for mon in range(0, numMonitors):
				d = dict()
				q = 0
				for a in AP:
					if(mon in num2[q]):
						if(a in ti):
							d.update({a : 'T'})
						else:
							d.update({a : 'F'})
					else:
						d.update({a : '?'})
					q = q + 1
				parView[numComm - 1][mon] = d

		#parView for each monitor
		#binomial distribution(0.1)
		if(readDist == "binomial"):
			for a in range(0, len(AP)):
				while(True):
					num2[a] = np.random.binomial(1, 0.1, numMonitors)
					if(1 in num2[a]):
						break;
			for mon in range(0, numMonitors):
				d = dict()
				q = 0
				for a in AP:
					if(mon in num2[q]):
						if(a in ti):
							d.update({a : 'T'})
						else:
							d.update({a : 'F'})
					else:
						d.update({a : '?'})
					q = q + 1
				parView[numComm - 1][mon] = d

		#Eqn 1
		for mon in range(0, numMonitors):
			QcurrentNextAll[mon] = list()
			Qcurrent = list()
			for i in range(0, len(AP)):
				Qcurrent.append(list())
			for tr in transitions:
				if(tr['from'] in QcurrentAll[mon]):
					i = -1
					for a in AP:
						i = i + 1
						flag = 0
						for s in tr['s']:
							if(parView[numComm - 1][mon][a] == 'T' and a in s):
								flag = 1
							elif(parView[numComm - 1][mon][a] == '?'):
								flag = 1
							elif(parView[numComm - 1][mon][a] == 'F' and not(a in s)):
								flag = 1
						if(flag == 1):
							Qcurrent[i].append(tr['to'])
			if(i > 0):
				QcurrentNextAll[mon] = Qcurrent[0]
				for i in range(1, len(AP)):
					QcurrentNextAll[mon] = intersection(Qcurrent[i], QcurrentNextAll[mon])

		#monitor crash
		crashMon = [0] * numMonitors
		crash = crash1 = crash2 = 0
		if(np.random.binomial(1, p) == 1):
			crash = min(abs(int(np.random.normal(0, 1.5))), kCrash - numCrash)
			crash1 = int(np.random.uniform(0, crash))
			crash2 = crash - crash1
		cr = 0
		if(crash1 > 0 ):
			for i in range(0, crash1):
				for j in range(0, 2 * numMonitors):
					mon = int(np.random.uniform(0, numMonitors))
					if(crashMon[mon] == 0):
						flagComm = 0
						for comm in range(0, numComm):
							flag = 0
							for a in AP:
								for mon1 in range(0, numMonitors):
									if(parView[comm][mon1][a] == parView[comm][mon][a] and not(parView[comm][mon][a] == '?') and not(mon == mon1)):
										flag = flag + 1
										break
								else:
									flag = -1
							if(flag == len(AP)):
								flagComm = flagComm + 1
							#crashArr[pos] = crashArr[pos] + 1
						if(flagComm == numComm):
							crashMon[mon] = 1
							numCrash = numCrash + 1 
							cr = cr + 1
							break

		if(numComm < kRound):
			for mon1 in range(0, numMonitors):
				QcurrentAll[mon1] = intersection(QcurrentNextAll[mon1], QcurrentNextAll[mon1])
			continue

		#Eqn 2
		for round in range(0, kCrash - numCrash + 1):
			numRnds = numRnds + 1
			for mon1 in range(0, numMonitors):
				if(crashMon[mon1] == 0):
					QcurrentAll[mon1] = list(set(QcurrentNextAll[mon1]))
					for mon2 in range(0, numMonitors):
						if(crashMon[mon2] == 0):
							numMsg = numMsg + 1
							msgSize = msgSize + sys.getsizeof(QcurrentNextAll[mon2])
							QcurrentAll[mon1] = intersection(QcurrentAll[mon1], QcurrentNextAll[mon2])
					if(crash2 > 0):
						r = np.random.binomial(1, 0.1)
						if(r == 1):
							flagComm = 0
							for comm in range(0, numComm):
								flag = 0
								for a in AP:
									for mon3 in range(0, numMonitors):
										if(parView[comm][mon3][a] == parView[comm][mon1][a] and not(parView[comm][mon1][a] == '?') and not(mon1 == mon3)):
											flag = flag + 1
											break
									else:
										flag = -1
								if(flag == len(AP)):
									flagComm = flagComm + 1
								#crashArr[pos] = crashArr[pos] + 1
							if(flagComm == numComm):
								crashMon[mon1] = 1
								numCrash = numCrash + 1 
								cr = cr + 1
								break
		numComm = 0
		parView = [[dict()] * numMonitors] * kRound

		#cleaning the crashed monitors
		pos = pos + 1
		i = 0
		for mon in range(0, numMonitors):
			if(crashMon[mon] == 1):
				QcurrentAll.remove(QcurrentAll[mon - i])
				QcurrentNextAll.remove(QcurrentNextAll[mon - i])
				i = i + 1
		numMonitors = numMonitors - cr

	'''print("RESULT")
	for mon in range(0, numMonitors):
		if(crashMon[mon] == 0):
			print(str(mon) + " : " + str(QcurrentAll[mon]))
			print(" : " + lambdaq[QcurrentAll[mon][0]])'''
	print(str(numRnds/len(trace)) + " ")
	print(" " + str(numMsg) + " ") 
	print(" " + str(msgSize/numMsg) + " ")
	print(" " + str(numCrash))
	#print(" " + '-'.join(map(str, crashArr)))

if __name__ == "__main__":
	if(len(sys.argv) == 7):
		main(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], float(sys.argv[6]))
	else:
		print("Not a valid argument")
		print("Valid Arguments:")
		print("<int1> fileName <int2> <int3> <string> <float> \t A system with <int1> number of monitors with <int2> number of maximum crashes, communicating after every <int3> rounds,  <string> read distribution and a binomial crash distribution with <float> parameter")