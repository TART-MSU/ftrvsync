def main():
    file = open("fileWrite.txt", "w")
    file.write("digraph G {\n")
    allStr = getAll("abcdefghi", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0])
    # allStr = getAll("abcdefg", 0, [0, 0, 0, 0, 0, 0, 0])

    for str1 in allStr:
        writeStr = ""
        if str1 == "":
            writeStr = "<empty>"
        else:
            for s in str1:
                writeStr = writeStr + "&&" + s
            writeStr = writeStr[2:]
        file.write("\"(0, 0)\" -> \"(1, 1)\" [label = \"(" + writeStr + ")\"]\n")

    States = []
    for i in range(1, int(len(allStr)/2) + 1):
        States = States + ["(" + str(i) + ", -1)"]

    idx = -1
    for i in range(len(allStr)):
        if i % 2 == 0:
            idx = idx + 1
        writeStr = ""
        if allStr[i] == "":
            writeStr = "(<empty>)"
            file.write("\"(1, 1)\" -> \"(0, 0)\" [label = \"" + writeStr + "\"]\n")
        else:
            for s in allStr[i]:
                writeStr = writeStr + "&&" + s
            writeStr = writeStr[2:]
            file.write("\"(1, 1)\" -> \"" + States[idx] + "\" [label = \"(" + writeStr + ")\"]\n")

    for toState in States:
        idx = -1
        for i in range(len(allStr)):
            if i % 2 == 0:
                idx = idx + 1
            writeStr = ""
            if allStr[i] == "":
                writeStr = "(<empty>)"
                file.write("\"" + toState + "\" -> \"(0, 0)\" [label = \"" + writeStr + "\"]\n")
            else:
                for s in allStr[i]:
                    writeStr = writeStr + "&&" + s
                writeStr = writeStr[2:]
                file.write("\"" + toState + "\" -> \"" + States[idx] + "\" [label = \"(" + writeStr + ")\"]\n")

    file.write("\"(0, 0)\" [label=\"(0, 0)\", style=filled, color=yellow]\n")
    file.write("\"(1, 1)\" [label=\"(1, 1)\", style=filled, color=yellow]\n")
    for toState in States:
        file.write("\"" + toState + "\" [label=\"" + toState + "\", style=filled, color=green]\n")
    file.write("}")
    file.close()


def getAll(str1, n, arr):
    if n == len(str1):
        str2 = ""
        for a in range(0, len(arr)):
            if arr[a] == 1:
                str2 = str2 + str1[a]
        return [str2]
    arr[n] = 1
    allStr1 = getAll(str1, n + 1, arr)
    arr[n] = 0
    allStr2 = getAll(str1, n + 1, arr)
    return list(allStr1 + allStr2)


if __name__ == "__main__":
    main()
