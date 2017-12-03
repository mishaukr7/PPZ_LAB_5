import heapq


def identity(numRows, numCols, val=1, rowStart=0):
   return [[(val if i == j else 0) for j in range(numCols)]
               for i in range(rowStart, numRows)]


def standardForm(cost,
                 greaterThans=[],
                 gtThreshold=[],
                 lessThans=[],
                 ltThreshold=[],
                 equalities=[],
                 eqThreshold=[],
                 maximization=True):
    newVars = 0
    numRows = 0
    if gtThreshold != []:
        newVars += len(gtThreshold)
        numRows += len(gtThreshold)
    if ltThreshold != []:
        newVars += len(ltThreshold)
        numRows += len(ltThreshold)
    if eqThreshold != []:
        numRows += len(eqThreshold)

    if not maximization:
        cost = [-x for x in cost]

    if newVars == 0:
        return cost, equalities, eqThreshold

    newCost = list(cost) + [0] * newVars

    constraints = []
    threshold = []

    oldConstraints = [(greaterThans, gtThreshold, -1), (lessThans, ltThreshold, 1),
                     (equalities, eqThreshold, 0)]

    offset = 0
    for constraintList, oldThreshold, coefficient in oldConstraints:
        constraints += [c + r for c, r in zip(constraintList,
        identity(numRows, newVars, coefficient, offset))]

        threshold += oldThreshold
        offset += len(oldThreshold)

    return newCost, constraints, threshold


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def column(A, j):
    return [row[j] for row in A]


def transpose(A):
    return [column(A, j) for j in range(len(A[0]))]


def isPivotCol(col):
    return (len([c for c in col if c == 0]) == len(col) - 1) and sum(col) == 1


# assume the last m columns of A are the slack variables; the initial basis is
# the set of slack variables
def initialTableau(c, A, b):
    tableau = [row[:] + [x] for row, x in zip(A, b)]
    tableau.append([ci for ci in c] + [0])
    return tableau


def primalSolution(tableau):
   # the pivot columns denote which variables are used
    columns = transpose(tableau)
    indices = [j for j, col in enumerate(columns[:-1]) if isPivotCol(col)]

    return list(zip(indices, columns[-1]))


def objectiveValue(tableau):
    return -(tableau[-1][-1])


def canImprove(tableau):
    lastRow = tableau[-1]
    return any(x > 0 for x in lastRow[:-1])


# this can be slightly faster
def moreThanOneMin(L):
    if len(L) <= 1:
        return False

    x,y = heapq.nsmallest(2, L, key=lambda x: x[1])
    return x == y


def findPivotIndex(tableau):
    # pick first nonzero index of the last row
    column = [i for i,x in enumerate(tableau[-1][:-1]) if x > 0][0]

   # check if unbounded
    if all(row[column] <= 0 for row in tableau):
        raise Exception('Linear program is unbounded.')

   # check for degeneracy: more than one minimizer of the quotient
    quotients = [(i, r[-1] / r[column])
        for i,r in enumerate(tableau[:-1]) if r[column] > 0]

    if moreThanOneMin(quotients):
        raise Exception('Linear program is degenerate.')

   # pick row index minimizing the quotient
    row = min(quotients, key=lambda x: x[1])[0]
    return row, column


def pivotAbout(tableau, pivot):
    i, j = pivot

    pivotDenom = tableau[i][j]
    tableau[i] = [x / pivotDenom for x in tableau[i]]

    for k, row in enumerate(tableau):
        if k != i:
            pivotRowMultiple = [y * tableau[k][j] for y in tableau[i]]
            tableau[k] = [x - y for x,y in zip(tableau[k], pivotRowMultiple)]


def simplex(c, A, b):
    tableau = initialTableau(c, A, b)
    while canImprove(tableau):
      pivot = findPivotIndex(tableau)
      pivotAbout(tableau, pivot)
    return tableau, objectiveValue(tableau)


