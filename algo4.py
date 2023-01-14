import subprocess
import collections
import sys


def split(AP, transitions):
    cv = 0
    for p in AP:
        for s1 in transitions:
            for s2 in transitions:
                if (s1 == s2):
                    continue
                index1 = s1.find(p)
                index2 = s2.find(p)
                if ((index1 == -1 and index2 != -1) or (index1 != -1 and index2 == -1)):
                    cv += 1
    cv = cv / 2
    if (pow(2, cv) > len(transitions)):
        return 1
    else:
        return 0


def readFile(fileName):
    file = open(directory + fileName, "r")
    # contains ref and the name of the states - draft
    state = dict()
    # contains the transactions - draft
    trans = dict()
    # contains the transactions - final
    T = list()
    lambdaq = dict()
    # contains the states - final
    S = list()
    # contains all the combinations of the alphabet - Sigma*
    AP = list()
    # contains the alphabets - Sigma
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

        if ((first < second) and (second < arrow) and (arrow < third) and (third < fourth) and (fourth < label) and (label < fifth) and (fifth < sixth)):
            stateFrom = line[first + 1:second]
            stateTo = line[third + 1:fourth]
            s = line[fifth + 2:sixth - 1]
            if (not (stateFrom in state)):
                state[stateFrom] = 'q' + str(len(state))
            if (not (stateTo in state)):
                state[stateTo] = 'q' + str(len(state))
            trans[str(len(trans))] = {'from': state[stateFrom], 'to': state[stateTo], 's': s}

        label = line.find("label", second)
        style = line.find("style", label)
        color = line.find("color", style)

        if ((label < style) and (style < color)):
            st = line[first + 1:second]
            if (st == "(0, 0)"):
                start = state[st]
            colour = line[color + 6:len(line) - 2]
            if (colour == "green"):
                lambdaq[state[st]] = 'T'
            elif (colour == "yellow"):
                lambdaq[state[st]] = '?'
            else:
                lambdaq[state[st]] = 'F'

    for key, val in state.items():
        S.append(val)

    for st1 in S:
        for st2 in S:
            tr = []
            for key, val in trans.items():
                if (val['from'] == st1 and val['to'] == st2):
                    a = val['s'].replace('&&', '')
                    if (a == '<empty>'):
                        a = ''
                    tr.append(a)
                    if (not (a in AP)):
                        AP.append(a)
            T.append({'from': st1, 'to': st2, 's': tr})
    for a in AP:
        for b in a:
            if (not (b in Sq)):
                Sq.append(b)

    return S, T, AP, Sq, lambdaq, start


def writeFile(state, transitions, lambdaq, start, fileName):
    file = open(fileName, "w")
    file.write("digraph G {")
    file.write("\n")

    # the ref to each states
    S = dict()
    # the transactions for each change
    T = dict()
    countA = countB = countC = 1
    for st in state:
        if (lambdaq[st] == '?'):
            if (st == start):
                S[st] = {'state': '(' + str(0) + ', ' + str(0) + ')', 'color': 'yellow'}
            else:
                S[st] = {'state': '(' + str(countA) + ', ' + str(countA + 1) + ')', 'color': 'yellow'}
                countA = countA + 1
        elif (lambdaq[st] == 'F'):
            S[st] = {'state': '(' + str(-1) + ', ' + str(countB) + ')', 'color': 'red'}
            countB = countB + 1
        else:
            S[st] = {'state': '(' + str(countC) + ', ' + str(-1) + ')', 'color': 'green'}
            countC = countC + 1

    for val in transitions:
        for tr in val['s']:
            if (tr == ''):
                stateFrom = S[val['from']]
                stateTo = S[val['to']]
                T[str(len(T))] = {'from': stateFrom['state'], 'to': stateTo['state'], 's': '<empty>'}
            else:
                str1 = tr[0]
                for a in tr[1:]:
                    str1 = str1 + '&&' + a
                stateFrom = S[val['from']]
                stateTo = S[val['to']]
                T[str(len(T))] = {'from': stateFrom['state'], 'to': stateTo['state'], 's': str1}

    for key, val in T.items():
        file.write("\"" + val['from'] + "\" -> \"" + val['to'] + "\" [label = \"(" + val['s'] + ")\"];")
        file.write("\n")

    for key, val in S.items():
        stateFrom = S[key]
        file.write("\"" + stateFrom['state'] + "\" [label=\"" + stateFrom['state'] + "\", style=filled, color=" + val['color'] + "]")
        file.write("\n")
    file.write("}")
    file.close()


def getL(transitions, stateFrom, stateTo):
    trans = list()
    for val in transitions:
        if (val['from'] == stateFrom and val['to'] == stateTo):
            for a in val['s']:
                trans.append(a)
    return trans


def doLexist(transitions, stateFrom, stateTo, s):
    for val in transitions:
        if (val['from'] == stateFrom and val['to'] == stateTo and val['s'] == s):
            return 1
    return 0


def updateL(transitions, stateFrom, stateTo, s):
    transitions.append({'from': stateFrom, 'to': stateTo, 's': s})
    return transitions


def getS(transitions, stateFrom, s):
    for val in transitions:
        if (val['from'] == stateFrom and val['s'] == s):
            return val['to']
    return ''


def getSFrom(transitions, stateTo):
    ans = list()
    i = 0
    for val in transitions:
        if (val['to'] == stateTo):
            ans.append({'from': val['from'], 's': val['s']})
            i = i + 1
    return ans


def copyL(transitions, trans, stateTo):
    for val in trans:
        transitions.append({'from': val['from'], 'to': stateTo, 's': val['s']})
    return transitions


def getStatesTo(transitions, stateFrom):
    stateTo = list()
    for val in transitions:
        if (val['from'] == stateFrom):
            stateTo.append(val['to'])
    return stateTo


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
            if (transitions[j].find(AP[i]) != -1):
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
        variables = variables + "\n" + "(declare-const v" + str(i + 1) + str(1) + " Bool)"
        variables = variables + "\n" + "(assert (= v" + str(i + 1) + str(1) + " (or y" + str(i + 1) + str(1) + " yn" + str(i + 1) + str(1) + ")))"
        variables = variables + "\n" + "(declare-const v" + str(i + 1) + str(2) + " Bool)"
        variables = variables + "\n" + "(assert (= v" + str(i + 1) + str(2) + " (or y" + str(i + 1) + str(2) + " yn" + str(i + 1) + str(2) + ")))"
    variables = variables + "\n"
    for i in range(len(transitions)):
        variables = variables + "\n" + "(declare-const w" + str(i + 1) + str(1) + " Int)"
        variables = variables + "\n" + "(assert(=> (= v" + str(i + 1) + str(1) + " true) (= w" + str(i + 1) + str(1) + " 0)))"
        variables = variables + "\n" + "(assert(=> (= v" + str(i + 1) + str(1) + " false) (= w" + str(i + 1) + str(1) + " 1)))"
        variables = variables + "\n" + "(declare-const w" + str(i + 1) + str(2) + " Int)"
        variables = variables + "\n" + "(assert(=> (= v" + str(i + 1) + str(2) + " true) (= w" + str(i + 1) + str(2) + " 0)))"
        variables = variables + "\n" + "(assert(=> (= v" + str(i + 1) + str(2) + " false) (= w" + str(i + 1) + str(2) + " 1)))"

    objective = objective + "\n" + "(minimize (+"
    for i in range(len(transitions)):
        objective = objective + " w" + str(i + 1) + str(1) + " w" + str(i + 1) + str(2)
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


def main(fileNameRead, fileNameWrite):
    # AP = ['a', 'b']
    # S = ['', 'a', 'b', 'ab']
    # transitions = [{'from':'q0', 'to':'q0', 's':['']},
    # {'from':'q0', 'to':'q1', 's':['a', 'b', 'ab']},
    # {'from':'q1', 'to':'q1', 's':['', 'a', 'b', 'ab']}
    # ]
    # transitions = [{'from':'q0', 'to':'q0', 's':['a', 'b', '']},
    # {'from':'q0', 'to':'q1', 's':['ab']}
    # ]
    transitionsq = list()
    statesRemove = list()
    print(fileNameWrite)
    # states = ['q0', 'q1']
    # start = 'q0'
    # lambdaq = {'q0':'?', 'q1':'T'}

    states, transitions, S, AP, lambdaq, start = readFile(fileNameRead)
    print(transitions)
    print(states)
    print(start)
    print(lambdaq)
    stateCounter = len(states)
    print("START")
    for stateFrom in states:
        statesTo = getStatesTo(transitions, stateFrom)
        for stateTo in statesTo:
            T = getL(transitions, stateFrom, stateTo)
            # print(str(stateFrom) + " " + str(stateTo) + " " + str(T))
            if (T == []):
                continue
            if (collections.Counter(T) == collections.Counter(S) or len(T) == 1):
                transitionsq.append({'from': stateFrom, 'to': stateTo, 's': T})
                continue
            createZ3(AP, T)
            cmdResult = subprocess.run(["z3", "z3-script"], stdout=subprocess.PIPE)
            z3Result = cmdResult.stdout.decode('utf-8')
            trans1 = []
            trans2 = []
            print("Hello")
            print(z3Result)
            for i in range(len(T)):
                pos = z3Result.index("x1" + str(i + 1))
                if (z3Result.index("true", pos) > z3Result.index("false", pos)):
                    trans1.append(T[i])
                else:
                    trans2.append(T[i])
            # trans1 and trans2 are the two transitions that the original is broken to

            if (split(AP, T)):
                # print("SPLIT")
                if (trans1 != T and trans2 != T):
                    # print("SPLIT-SMT")
                    # print(trans1)
                    # print(trans2)
                    q1 = 'q' + str(stateCounter)
                    q2 = 'q' + str(stateCounter + 1)
                    stateCounter = stateCounter + 2
                    states.append(q1)
                    states.append(q2)
                    statesRemove.append(stateTo)
                    # states.remove(stateTo)
                    # states updated

                    lambdaq[q1] = lambdaq[stateTo]
                    lambdaq[q2] = lambdaq[stateTo]
                    if (not (stateFrom == stateTo)):
                        # print("DIFFERENT NODES")
                        transitions.append({'from': stateFrom, 'to': q1, 's': trans1})
                        transitions.append({'from': stateFrom, 'to': q2, 's': trans2})
                        statesTo.append(q1)
                        statesTo.append(q2)

                        for val in transitions.copy():
                            # print(str(val['from']) + " " + str(val['to']) + " " + str(val['s']))
                            if (str(val['from']) == str(stateTo)):
                                if (str(val['to']) == str(stateTo)):
                                    transitions.append({'from': q1, 'to': q1, 's': val['s']})
                                    transitions.append({'from': q2, 'to': q2, 's': val['s']})
                                    transitions.remove(val)
                                else:
                                    transitions.append({'from': q1, 'to': val['to'], 's': val['s']})
                                    transitions.append({'from': q2, 'to': val['to'], 's': val['s']})
                                    transitions.remove(val)

                        for val in transitionsq.copy():
                            if (val['from'] == stateTo):
                                if (val['to'] == stateTo):
                                    transitionsq.append({'from': q1, 'to': q1, 's': val['s']})
                                    transitionsq.append({'from': q2, 'to': q2, 's': val['s']})
                                    transitionsq.remove(val)
                                else:
                                    transitionsq.append({'from': q1, 'to': val['to'], 's': val['s']})
                                    transitionsq.append({'from': q2, 'to': val['to'], 's': val['s']})
                                    transitionsq.remove(val)

                    else:
                        # print("SAME NODES")
                        transitions.append({'from': q1, 'to': q1, 's': trans1})
                        transitions.append({'from': q2, 'to': q1, 's': trans1})
                        transitions.append({'from': q1, 'to': q2, 's': trans2})
                        transitions.append({'from': q2, 'to': q2, 's': trans2})

                        for val in transitions.copy():
                            if (val['from'] == stateTo and val['s'] != T):
                                transitions.append({'from': q1, 'to': val['to'], 's': val['s']})
                                transitions.append({'from': q2, 'to': val['to'], 's': val['s']})
                                transitions.remove(val)

                        for val in transitionsq.copy():
                            if (val['from'] == stateTo and val['s'] != T):
                                transitionsq.append({'from': q1, 'to': val['to'], 's': val['s']})
                                transitionsq.append({'from': q2, 'to': val['to'], 's': val['s']})
                                transitionsq.remove(val)

                    for val in transitions.copy():
                        if (val['to'] == stateTo):
                            if (val['from'] != stateFrom):
                                transitions.append({'from': val['from'], 'to': q1, 's': val['s']})
                                transitions.append({'from': val['from'], 'to': q2, 's': val['s']})
                                transitions.remove(val)

                    for val in transitionsq.copy():
                        if (val['to'] == stateTo):
                            if (val['from'] != stateFrom):
                                transitionsq.append({'from': val['from'], 'to': q1, 's': val['s']})
                                transitionsq.append({'from': val['from'], 'to': q2, 's': val['s']})
                                transitionsq.remove(val)

                    if (stateTo == start):
                        start = q1

                else:
                    # print("NOT SPLIT - SMT")
                    transitionsq.append({'from': stateFrom, 'to': stateTo, 's': T})
            else:
                # print("NOT SPLIT")
                transitionsq.append({'from': stateFrom, 'to': stateTo, 's': T})

    for st in states:
        if st in statesRemove:
            states.remove(st)
            del lambdaq[st]

    print("RESULTS")
    print(transitionsq)
    print(states)
    print(lambdaq)
    print(start)
    writeFile(states, transitionsq, lambdaq, start, fileNameWrite)


if __name__ == "__main__":
    directory = "formulaFiles/"
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Not a valid argument")
        print("Valid Arguments:")
        print("fileNameRead fileNameWrite \t Read a FSM from fileNameRead and write to fileNameWrite with the required changes")
