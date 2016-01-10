#!/usr/bin/env python
"""
This script will plot
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

def size(IN):
    M = len(IN[0])
    N = len(IN)
    return (M, N)

def NumberOfRuns(IN):
    M, N = size(IN)
    result = 0
    if M != 0 and N != 0:
        for col in IN:
            if col[0] != 0:
                result += 1
            for idx in range(1, M):
                if col[idx] != 0 and col[idx-1] == 0:
                    result += 1
    return result

def FillRunVectors(IN):
    M, N = size(IN)
    c = []
    sr = []
    er = []
    for cidx ,col in enumerate(IN):
        k = 0
        while k < M:
            try:
                k += col[k:].index(1)
                c.append(cidx+1)
                sr.append(k+1) #! for matlab
                try:
                    k += col[k:].index(0)
                except ValueError:
                    k = M
                er.append(k)
            except ValueError:
                break
    return sr, er, c

def FirstPass(numRuns, mode, sr, er, c):
    currentColumn = 0
    nextLabel = 1
    firstRunOnPreviousColumn = -1
    lastRunOnPreviousColumn = -1
    firstRunOnThisColumn = -1
    equivList = []
    labels = [0] * numRuns
    if mode == 8:
        offset = 1
    else:
        offset = 0
    for k in range(numRuns):
        if c[k] == currentColumn + 1:
            firstRunOnPreviousColumn = firstRunOnThisColumn
            firstRunOnThisColumn = k
            lastRunOnPreviousColumn = k-1
            currentColumn = c[k]
        elif c[k] > currentColumn+1:
            firstRunOnPreviousColumn = -1
            lastRunOnPreviousColumn = -1
            firstRunOnThisColumn = k
            currentColumn = c[k]
        else:
            pass
        if firstRunOnPreviousColumn >= 0:
            p = firstRunOnPreviousColumn
            while p<=lastRunOnPreviousColumn and sr[p]<=er[k]+offset:
                if er[k]>=sr[p]-offset and sr[k]<=er[p]+offset:
                    if labels[k] == 0:
                        labels[k] = labels[p]
                    else:
                        if labels[k] != labels[p]:
                            equivList.insert(0, (labels[k],labels[p]))
                        else:
                            pass
                p += 1
        if labels[k] == 0:
            labels[k] = nextLabel
            nextLabel += 1
    rowEquivalences = []
    colEquivalences = []
    if len(equivList) > 0:
        for item0, item1 in equivList:
            rowEquivalences.append(item0)
            colEquivalences.append(item1)
    return labels, rowEquivalences, colEquivalences

def bwlabel1(BW, mode=8):
    BW = list(BW)
    for k in range(len(BW)):
        BW[k] = list(BW[k])
    numRuns = NumberOfRuns(BW)
    sr, er, c = FillRunVectors(BW)
    labels, rowEquivalences, colEquivalences = FirstPass(numRuns, mode, sr, er, c)
    return sr, er, c, labels, rowEquivalences, colEquivalences