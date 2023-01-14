import subprocess
import os
import sys
import numpy as np
from scipy.stats import sem, t
import xlsxwriter


def body0():
    dist = ""
    p = 0
    numIter = 40

    for kRound in [1, 2, 3, 5, 8, 10, 15, 20, 35, 50]:
        for j in [8]:
            print("+++++++++++++++++++++++++++++++++++++:kRound: " + str(kRound) + ":++++++++++++++++++++++++++++++++++++")
            if j == 0 or j == 4 or j == 8:
                dist = "uniform"
                p = 0.5
            elif j == 1 or j == 5 or j == 9:
                dist = "binomial"
                p = 0.5
            elif j == 2 or j == 6 or j == 10:
                dist = "binomial"
                p = 0.9
            else:
                dist = "uniform"
                p = 0.1

            workbook = xlsxwriter.Workbook("report" + str(j) + "_" + str(kRound) + ".xlsx")
            worksheet = workbook.add_worksheet()
            row = 0
            fnum = list(range(0, 38))
            fnum.extend(list(range(40, 48)))
            fnum.extend(list(range(50, 53)))

            for num in [4]:
                print("--------------------------------:Formula Number: " + str(num + 1) + ":--------------------------------")
                worksheet.write(row, 0, "Formula Number: " + str(num))
                row = row + 1
                worksheet.write(row, 0, "Monitor")
                worksheet.write(row, 1, "Max Crash")
                worksheet.write(row, 2, "Rounds")
                worksheet.write(row, 3, "Rounds error")
                worksheet.write(row, 4, "Msg")
                worksheet.write(row, 5, "Msg error")
                worksheet.write(row, 6, "Size")
                worksheet.write(row, 7, "Size error")
                worksheet.write(row, 8, "Crash")
                worksheet.write(row, 9, "Crash error")
                row = row + 1

                for mon in [10, 20, 30]:
                    if mon == 10:
                        crList = [4, 5, 6, 7, 8]
                    elif mon == 20:
                        crList = [10, 12, 14, 16, 18]
                    else:
                        crList = [10, 15, 20, 25, 28]

                    for crash in crList:
                        rounds = [0] * numIter
                        msg = [0] * numIter
                        size = [0] * numIter
                        crashNum = [0] * numIter

                        i = 0
                        while i < numIter:
                            s1 = subprocess.getstatusoutput("python3 pattern.py " + str(num) + " text" + str(num) + ".txt")

                            formula = str(s1[1])
                            AP = "["
                            for alpha in formula:
                                if alpha.isalpha() == True and not (alpha == 'X' or alpha == 'U') and not (alpha in AP):
                                    AP = AP + alpha
                            AP = AP + "]"

                            if j < 4:
                                s2 = subprocess.getstatusoutput("python3 trace.py flipCoin 100 " + AP + " trace.txt")
                            elif 3 < j < 8:
                                s2 = subprocess.getstatusoutput("python3 trace.py bernouilli 0.1 100 " + AP + " trace.txt")
                            else:
                                s2 = subprocess.getstatusoutput("python3 trace.py bernouilli 0.9 100 " + AP + " trace.txt")

                            # s3 = subprocess.getstatusoutput("python3 algo4.py text" + str(num) + ".txt textNew" + str(num) + ".txt")

                            s4 = subprocess.getstatusoutput("python3 monitor.py " + str(mon) + " textNew" + str(num) + ".txt " + str(crash) + " " + str(kRound) + " " + dist + " " + str(p))

                            try:
                                flag = 0
                                j = -1
                                for a in s4:
                                    if not (j == -1):
                                        for b in a.split():
                                            if j == 0:
                                                rounds[i] = float(b)
                                                if rounds[i] > 1 or kRound > 1:
                                                    flag = 1
                                            elif j == 1:
                                                msg[i] = float(b)
                                            elif j == 2:
                                                size[i] = float(b)
                                            else:
                                                crashNum[i] = float(b)
                                            j = j + 1
                                    else:
                                        j = 0
                                i = i + flag
                            except:
                                continue

                        mRounds = np.mean(rounds)
                        stdErrRounds = sem(rounds)
                        errRounds = stdErrRounds * t.ppf((1 + 0.95) / 2, numIter - 1)
                        mMsg = np.mean(msg)
                        stdErrMsg = sem(msg)
                        errMsg = stdErrMsg * t.ppf((1 + 0.95) / 2, numIter - 1)
                        mSize = np.mean(size)
                        stdErrSize = sem(size)
                        errSize = stdErrSize * t.ppf((1 + 0.95) / 2, numIter - 1)
                        mCrash = np.mean(crashNum)
                        stdErrCrash = sem(crashNum)
                        errCrash = stdErrCrash * t.ppf((1 + 0.95) / 2, numIter - 1)

                        print("Monitor: " + str(mon) + " &&&&&&&&&&& Crash: " + str(crash))
                        print("Average Number of Rounds: " + str(mRounds) + " Confidence Error: " + str(errRounds))
                        print("Total number of messages: " + str(mMsg) + " Confidence Error: " + str(errMsg))
                        print("Average size of a message: " + str(mSize) + " Confidence Error: " + str(errSize))
                        print("Average number of crashes: " + str(mCrash) + " Confidence Error: " + str(errCrash))

                        worksheet.write(row, 0, str(round(mon, 2)))
                        worksheet.write(row, 1, str(round(crash, 2)))
                        worksheet.write(row, 2, str(round(mRounds, 2)))
                        worksheet.write(row, 3, str(round(errRounds, 2)))
                        worksheet.write(row, 4, str(round(mMsg, 2)))
                        worksheet.write(row, 5, str(round(errMsg, 2)))
                        worksheet.write(row, 6, str(round(mSize, 2)))
                        worksheet.write(row, 7, str(round(errSize, 2)))
                        worksheet.write(row, 8, str(round(mCrash, 2)))
                        worksheet.write(row, 9, str(round(errCrash, 2)))
                        row = row + 1

                        sys.stdout.flush()
        workbook.close()


def body1(num):
    kRound = 5
    workbook = xlsxwriter.Workbook('report.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    worksheet.write(row, 0, "Monitor")
    worksheet.write(row, 1, "Max Crash")
    worksheet.write(row, 2, "Rounds")
    worksheet.write(row, 3, "Rounds error")
    worksheet.write(row, 4, "Msg")
    worksheet.write(row, 5, "Msg error")
    worksheet.write(row, 6, "Size")
    worksheet.write(row, 7, "Size error")
    worksheet.write(row, 8, "Crash")
    worksheet.write(row, 9, "Crash error")
    row = row + 1

    for mon in [10, 20, 30]:
        if mon == 10:
            crList = [4, 5, 6, 7, 8]
        elif mon == 20:
            crList = [10, 12, 14, 16, 18]
        else:
            crList = [10, 15, 20, 25, 28]

        for crash in crList:
            rounds = [0] * 20
            msg = [0] * 20
            size = [0] * 20
            crashNum = [0] * 20

            i = 0
            while i < 20:
                s1 = subprocess.getstatusoutput("python3 pattern.py " + str(num) + " text" + str(num) + ".txt")

                formula = str(s1[1])
                AP = "["
                for alpha in formula:
                    if alpha.isalpha() == True and not (alpha == 'X' or alpha == 'U') and not (alpha in AP):
                        AP = AP + alpha
                AP = AP + "]"

                s2 = subprocess.getstatusoutput("python3 trace.py flipCoin 100 " + AP + " trace.txt")
                # s2 = subprocess.getstatusoutput("python3 trace.py flipCoinChange 100 " + AP + " trace.txt")
                # s2 = subprocess.getstatusoutput("python3 trace.py bernouilli 0.1 100 " + AP + " trace.txt")

                # s3 = subprocess.getstatusoutput("python3 algo4.py text" + str(num) + ".txt textNew" + str(num) + ".txt")

                s4 = subprocess.getstatusoutput("python3 monitor.py " + str(mon) + " textNew" + str(num) + ".txt " + str(crash) + " " + str(kRound) + " uniform 0.5")
                # s4 = subprocess.getstatusoutput("python3 monitor.py " + str(mon)+ " textNew" + str(num) + ".txt " + str(crash) + " " + str(kRound) + " binomial 0.5")
                # s4 = subprocess.getstatusoutput("python3 monitor.py " + str(mon)+ " textNew" + str(num) + ".txt " + str(crash) + " " + str(kRound) + " binomial 0.9")
                # s4 = subprocess.getstatusoutput("python3 monitor.py " + str(mon)+ " textNew" + str(num) + ".txt " + str(crash) + " " + str(kRound) + " uniform 0.1")

                try:
                    flag = 0
                    j = -1
                    for a in s4:
                        if not (j == -1):
                            for b in a.split():
                                if j == 0:
                                    rounds[i] = float(b)
                                    if rounds[i] > 1 or kRound > 1:
                                        flag = 1
                                elif j == 1:
                                    msg[i] = float(b)
                                elif j == 2:
                                    size[i] = float(b)
                                else:
                                    crashNum[i] = float(b)
                                j = j + 1
                        else:
                            j = 0
                    i = i + flag
                except:
                    continue

            mRounds = np.mean(rounds)
            stdErrRounds = sem(rounds)
            errRounds = stdErrRounds * t.ppf((1 + 0.95) / 2, 20 - 1)
            mMsg = np.mean(msg)
            stdErrMsg = sem(msg)
            errMsg = stdErrMsg * t.ppf((1 + 0.95) / 2, 20 - 1)
            mSize = np.mean(size)
            stdErrSize = sem(size)
            errSize = stdErrSize * t.ppf((1 + 0.95) / 2, 20 - 1)
            mCrash = np.mean(crashNum)
            stdErrCrash = sem(crashNum)
            errCrash = stdErrCrash * t.ppf((1 + 0.95) / 2, 20 - 1)

            print("Monitor: " + str(mon) + " &&&&&&&&&&& Crash: " + str(crash))
            print("Average Number of Rounds: " + str(mRounds) + " Confidence Error: " + str(errRounds))
            print("Total number of messages: " + str(mMsg) + " Confidence Error: " + str(errMsg))
            print("Average size of a message: " + str(mSize) + " Confidence Error: " + str(errSize))
            print("Average number of crashes: " + str(mCrash) + " Confidence Error: " + str(errCrash))

            worksheet.write(row, 0, str(round(mon, 2)))
            worksheet.write(row, 1, str(round(crash, 2)))
            worksheet.write(row, 2, str(round(mRounds, 2)))
            worksheet.write(row, 3, str(round(errRounds, 2)))
            worksheet.write(row, 4, str(round(mMsg, 2)))
            worksheet.write(row, 5, str(round(errMsg, 2)))
            worksheet.write(row, 6, str(round(mSize, 2)))
            worksheet.write(row, 7, str(round(errSize, 2)))
            worksheet.write(row, 8, str(round(mCrash, 2)))
            worksheet.write(row, 9, str(round(errCrash, 2)))
            row = row + 1

            sys.stdout.flush()
    workbook.close()


def body2(num, mon, crash):
    kRound = 5
    rounds = [0] * 20
    msg = [0] * 20
    size = [0] * 20
    crashNum = [0] * 20

    i = 0
    while i < 20:
        print(i)
        s1 = subprocess.getstatusoutput("python3 pattern.py " + str(num) + " text" + str(num) + ".txt")

        formula = str(s1[1])
        AP = "["
        for alpha in formula:
            if alpha.isalpha() == True and not (alpha == 'X' or alpha == 'U') and not (alpha in AP):
                AP = AP + alpha
        AP = AP + "]"

        s2 = subprocess.getstatusoutput("python3 trace.py flipCoin 100 " + AP + " trace.txt")
        # s2 = subprocess.getstatusoutput("python3 trace.py flipCoinChange 100 " + AP + " trace.txt")
        # s2 = subprocess.getstatusoutput("python3 trace.py bernouilli 0.1 100 " + AP + " trace.txt")

        # s3 = subprocess.getstatusoutput("python3 algo4.py text" + str(num) + ".txt textNew" + str(num) + ".txt")

        s4 = subprocess.getstatusoutput("python3 monitor.py " + str(mon) + " textNew" + str(num) + ".txt " + str(crash) + " " + str(kRound) + " uniform 0.5")

        try:
            flag = 0
            j = -1
            for a in s4:
                if not (j == -1):
                    for b in a.split():
                        if j == 0:
                            rounds[i] = float(b)
                            if rounds[i] > 1 or kRound > 1:
                                flag = 1
                        elif j == 1:
                            msg[i] = float(b)
                        elif j == 2:
                            size[i] = float(b)
                        else:
                            crashNum[i] = float(b)
                        j = j + 1
                else:
                    j = 0
            i = i + flag
        except:
            print(s4)

    mRounds = np.mean(rounds)
    stdErrRounds = sem(rounds)
    errRounds = stdErrRounds * t.ppf((1 + 0.95) / 2, 20 - 1)
    mMsg = np.mean(msg)
    stdErrMsg = sem(msg)
    errMsg = stdErrMsg * t.ppf((1 + 0.95) / 2, 20 - 1)
    mSize = np.mean(size)
    stdErrSize = sem(size)
    errSize = stdErrSize * t.ppf((1 + 0.95) / 2, 20 - 1)
    mCrash = np.mean(crashNum)
    stdErrCrash = sem(crashNum)
    errCrash = stdErrCrash * t.ppf((1 + 0.95) / 2, 20 - 1)

    print("Monitor: " + str(mon) + " &&&&&&&&&&& Crash: " + str(crash))
    print("Average Number of Rounds: " + str(mRounds) + " Confidence Error: " + str(errRounds))
    print("Total number of messages: " + str(mMsg) + " Confidence Error: " + str(errMsg))
    print("Average size of a message: " + str(mSize) + " Confidence Error: " + str(errSize))
    print("Average number of crashes: " + str(mCrash) + " Confidence Error: " + str(errCrash))

    sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "all":
        body0()
    elif len(sys.argv) == 2 and sys.argv[1].isnumeric():
        body1(int(sys.argv[1]))
    elif len(sys.argv) == 4 and sys.argv[1].isnumeric() and sys.argv[2].isnumeric() and sys.argv[3].isnumeric():
        body2(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("Not a valid argument")
        print("Valid Arguments:")
        print("all \t Run all the different combinations and generate the report")
        print("<int> \t Run only on formula numbered <int>")
        print("<int1> <int2> <int3> \t Run only on formula number <int1> with <int2> monitors and t = <int3> crashes")
