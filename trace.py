import random
import sys

def genFlipCoin(numTrace, alpha, fileName):
	trace = list()
	for i in range(numTrace):
		str = ''
		for a in alpha:
			num = random.randint(0,2)
			if(num == 0):
				str = str + a
		trace.append(str)
	createFile(trace, fileName)
	return trace

def genFlipCoinChange(numTrace, alpha, fileName):
	trace = list()
	for i in range(numTrace):
		str = ''
		for a in alpha:
			num = random.randint(0,2)
			if(num == 0):
				str = str + a
		trace.append(str)
	createFile(trace, fileName)
	return trace

def genBernouilli(prob, numTrace, alpha, fileName):
	trace = list()
	num = prob
	num1 = str(prob)
	while(int(num) != num):
		num = num * 10
	num = int(num)
	num1 = pow(10, len(num1) - 2)

	for i in range(numTrace):
		str1 = ''
		for a in alpha:
			rNum = random.randint(0, num1)
			if(rNum <= num):
				str1 = str1 + a
		trace.append(str1)
	createFile(trace, fileName)

	return trace

def createFile(trace, fileName):
	file = open(fileName, "w")
	for line in trace:
		file.write(str(line))
		file.write("\n")
	file.close()

if __name__ == "__main__":
	AP = list()
	if(len(sys.argv) == 5 and sys.argv[1] == "flipCoin" and sys.argv[2].isnumeric()):
		for alpha in sys.argv[3]:
			if not(alpha == '[' or alpha == ']'):
				AP.append(alpha)
		print(genFlipCoin(int(sys.argv[2]), AP, sys.argv[4]))
	elif(len(sys.argv) == 5 and sys.argv[1] == "flipCoinChange" and sys.argv[2].isnumeric()):
		for alpha in sys.argv[3]:
			if not(alpha == '[' or alpha == ']'):
				AP.append(alpha)
		print(genFlipCoinChange(int(sys.argv[2]), AP, sys.argv[4]))
	elif(len(sys.argv) == 6 and sys.argv[1] == "bernouilli" and float(sys.argv[2]) > 0 and float(sys.argv[2]) < 1 and sys.argv[3].isnumeric()):
		for alpha in sys.argv[4]:
			if not(alpha == '[' or alpha == ']'):
				AP.append(alpha)
		print(genBernouilli(float(sys.argv[2]), int(sys.argv[3]), AP, sys.argv[5]))
	else:
		print("Not a valid argument")
		print("Valid Arguments:")
		print("flipCoin <int> <list> fileName \t flipcoin distribution to produce <int> traces and store in fileName file with <list> alphabets")
		print("flipCoinChange <int> <list> fileName \t flipcoin distribution - only change to produce <int> traces and store in fileName file with <list> alphabets")
		print("bernouilli <float> <int> <list> fileName\t Bernouilli distribution with <float> - only change; <float> should be a value between 0 and 1 to produce <int> traces and store in fileName file with <list> alphabets")