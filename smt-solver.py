import subprocess

def createZ3(AP, transitions):
	constants = "(echo \"Constants\")"
	function = "(echo \"Functions\")"
	variables = "(echo \"Variables\")"
	objective = "(echo \"Objective\")"

	for i in range(len(AP)):
		for j in range(len(transitions)):
			constants = constants + "\n" + "(declare-const a" + str(i + 1) + str(j + 1) + " Bool)"
	constants = constants + "\n"
	for i in range(len(AP)):
		for j in range(len(transitions)):
			if(transitions[j].find(AP[i]) != -1):
				constants = constants + "\n" + "(assert (= a" + str(i + 1) + str(j + 1) + " true))"
			else:
				constants = constants + "\n" + "(assert (= a" + str(i + 1) + str(j + 1) + " false))"

	function = function + "\n" + "(define-fun f1 ((x Bool) (a Bool)) Bool\n (ite (= x true) a true)\n)"

	for i in range(len(transitions)):
		variables = variables + "\n" + "(declare-const x" + str(1) + str(i + 1) + " Bool)"
		variables = variables + "\n" + "(declare-const x" + str(2) + str(i + 1) + " Bool)"
		variables = variables + "\n" + "(assert (= x" + str(2) + str(i + 1) + " (not x" + str(1) + str(i + 1) + ")))"
	variables = variables + "\n"
	for i in range(len(AP)):
		variables = variables + "\n" + "(declare-const y" + str(i + 1) + str(1) + " Bool)"
		variables = variables + "\n" + "(declare-const y" + str(i + 1) + str(2) + " Bool)"
		variables = variables + "\n" + "(declare-const yn" + str(i + 1) + str(1) + " Bool)"
		variables = variables + "\n" + "(declare-const yn" + str(i + 1) + str(2) + " Bool)"
	variables = variables + "\n"
	for i in range(len(AP)):
		variables = variables + "\n" + "(assert (=> (= (and"
		for j in range(len(transitions)):
			variables = variables + " (f1 x" + str(1) + str(j + 1) + " a" + str(i + 1) + str(j + 1) + ")"
		variables = variables + ") true) (= y" + str(i + 1) + str(1) + " true)))"
		variables = variables + "\n" + "(assert (=> (= (and"
		for j in range(len(transitions)):
			variables = variables + " (f1 x" + str(1) + str(j + 1) + " a" + str(i + 1) + str(j + 1) + ")"
		variables = variables + ") false) (= y" + str(i + 1) + str(1) + " false)))"
		variables = variables + "\n" + "(assert (=> (= (and"
		for j in range(len(transitions)):
			variables = variables + " (f1 x" + str(2) + str(j + 1) + " a" + str(i + 1) + str(j + 1) + ")"
		variables = variables + ") true) (= y" + str(i + 1) + str(2) + " true)))"
		variables = variables + "\n" + "(assert (=> (= (and"
		for j in range(len(transitions)):
			variables = variables + " (f1 x" + str(2) + str(j + 1) + " a" + str(i + 1) + str(j + 1) + ")"
		variables = variables + ") false) (= y" + str(i + 1) + str(2) + " false)))"
		variables = variables + "\n" + "(assert (=> (= (and"
		for j in range(len(transitions)):
			variables = variables + " (f1 x" + str(1) + str(j + 1) + " (not a" + str(i + 1) + str(j + 1) + "))"
		variables = variables + ") true) (= yn" + str(i + 1) + str(1) + " true)))"
		variables = variables + "\n" + "(assert (=> (= (and"
		for j in range(len(transitions)):
			variables = variables + " (f1 x" + str(1) + str(j + 1) + " (not a" + str(i + 1) + str(j + 1) + "))"
		variables = variables + ") false) (= yn" + str(i + 1) + str(1) + " false)))"
		variables = variables + "\n" + "(assert (=> (= (and"
		for j in range(len(transitions)):
			variables = variables + " (f1 x" + str(2) + str(j + 1) + " (not a" + str(i + 1) + str(j + 1) + "))"
		variables = variables + ") true) (= yn" + str(i + 1) + str(2) + " true)))"
		variables = variables + "\n" + "(assert (=> (= (and"
		for j in range(len(transitions)):
			variables = variables + " (f1 x" + str(2) + str(j + 1) + " (not a" + str(i + 1) + str(j + 1) + "))"
		variables = variables + ") false) (= yn" + str(i + 1) + str(2) + " false)))"
	variables = variables + "\n"
	for i in range(len(transitions)):
		variables = variables + "\n" + "(declare-const v" + str(i + 1) +  str(1) + " Bool)"
		variables = variables + "\n" + "(assert (= v" + str(i + 1) +  str(1) + " (or y" + str(i + 1) +  str(1) + " yn" + str(i + 1) +  str(1) + ")))"
		variables = variables + "\n" + "(declare-const v" + str(i + 1) +  str(2) + " Bool)"
		variables = variables + "\n" + "(assert (= v" + str(i + 1) +  str(2) + " (or y" + str(i + 1) +  str(2) + " yn" + str(i + 1) +  str(2) + ")))"
	variables = variables + "\n"
	for i in range(len(transitions)):
		variables = variables + "\n" + "(declare-const w" + str(i + 1) +  str(1) + " Int)"
		variables = variables + "\n" + "(assert(=> (= v" + str(i + 1) +  str(1) + " true) (= w" + str(i + 1) +  str(1) + " 0)))"
		variables = variables + "\n" + "(assert(=> (= v" + str(i + 1) +  str(1) + " false) (= w" + str(i + 1) +  str(1) + " 1)))"
		variables = variables + "\n" + "(declare-const w" + str(i + 1) +  str(2) + " Int)"
		variables = variables + "\n" + "(assert(=> (= v" + str(i + 1) +  str(2) + " true) (= w" + str(i + 1) +  str(2) + " 0)))"
		variables = variables + "\n" + "(assert(=> (= v" + str(i + 1) +  str(2) + " false) (= w" + str(i + 1) +  str(2) + " 1)))"

	objective = objective + "\n" + "(minimize (+"
	for i in range(len(transitions)):
		objective = objective + " w" + str(i + 1) +  str(1) + " w" + str(i + 1) +  str(2)
	objective = objective + "))"
	objective = objective + "\n" + "(check-sat)"
	objective = objective + "\n" + "(get-model)"
	objective = objective + "\n" + "(get-objectives)"

	file = open("z3-script", "w")
	file.write(constants)
	file.write("\n\n")
	file.write(function)
	file.write("\n\n")
	file.write(variables)
	file.write("\n\n")
	file.write(objective)
	file.close()

def split(AP, transitions):
	cv = 0
	for p in AP:
		for s1 in transitions:
			for s2 in transitions:
				if(s1 == s2):
					continue
				index1 = s1.find(p)
				index2 = s2.find(p)
				if((index1 == -1 and index2 != -1) or (index1 != -1 and index2 == -1)):
					cv += 1
	cv = cv / 2
	if(pow(2, cv) > len(transitions)):
		return 1
	else:
		return 0

if __name__ == "__main__":
	AP = ['a', 'b', 'c']
	T = ['a', 'ab', 'ac']
	if(split(AP, T)):
		print("SPLIT")
		createZ3(AP, T)
		cmdResult = subprocess.run(["z3", "z3-script"], stdout = subprocess.PIPE)
		z3Result = cmdResult.stdout.decode('utf-8')
		trans1 = []
		trans2 = []
		for i in range(len(T)):
			pos = z3Result.index("x1" + str(i + 1))
			if(z3Result.index("true", pos) > z3Result.index("false", pos)):
				trans1.append(T[i])
			else:
				trans2.append(T[i])
		print(trans1)
		print(trans2)
	else:
		print("NOT SPLIT")