import simplex


c = [6, 6]
A = [[2, 0], [1, 2], [1, 4]]
b = [20, 37, 30]

# add slack variables by hand
A[0] += [1, 0, 0]
A[1] += [0, 1, 0]
A[2] += [0, 0, 1]
c += [0, 0, 0]

t, s, v = simplex.simplex(c, A, b)
print('', t[0], '\n', t[1], '\n', t[2], '\n', t[3])
print(s)
print(v)