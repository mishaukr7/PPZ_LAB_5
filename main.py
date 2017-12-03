import simplex


def main():
    while True:
        try:
            number_of_values = int(input('Input number of variables: '))
            break
        except ValueError:
            print("ERROR! Number of values - must be integer value. Try again...")

    while True:
        try:
            number_of_constraint = int(input('Input number of constraints: '))
            break
        except ValueError:
            print("ERROR! Number of constraints - must be integer value. Try again...")

    function_coefficient = []
    while True:
        try:
            print('Input coefficient of function F(t):')
            for i in range(number_of_values):
                t = float(input("Enter t_{0}: ".format(i + 1)))
                function_coefficient.append(t)
            break
        except ValueError:
            print("ERROR! Coefficient of function must be float value. Try again...")

    matrix_A = []
    while True:
        try:
            print('Enter matrix A - array of coefficients of the left part of the constraints ')
            for i in range(number_of_constraint):
                a = []
                for j in range(number_of_values):
                    a.append(float(input('Enter a_{0}_{1}: '.format(i+1, j+1))))
                matrix_A.append(a)
            break
        except ValueError:
            print('ERROR! Coefficient of constraints must be float value. Try again...')

    maximum_b = []
    while True:
        try:
            print('Input value of the right part of the constraints:')
            for i in range(number_of_constraint):
                b = float(input("Enter b_{0}: ".format(i + 1)))
                maximum_b.append(b)
            break
        except ValueError:
            print("ERROR! Coefficient of function must be float value. Try again...")
    for i in range(0, number_of_constraint):
        additional_list = [0]*number_of_constraint
        additional_list[i] = 1
        matrix_A[i] += additional_list
    function_coefficient += [0]*number_of_constraint
    t, v = simplex.simplex(function_coefficient, matrix_A, maximum_b)
    print('-'*30)
    print('RESULT:')
    print('END SIMPLEX TABLE:')
    #[print(x) for x in t]
    for row in t:
        new_row = []
        for i in range(-1, 2*number_of_constraint-1):
            new_row.append(row[i])
        print(new_row)
    print('Point of maximum:')
    list_counter = []
    # for row in t:
    #     i = 1
    #     if t.index(row) < number_of_values-1:
    #         list_counter.append(t.index(row))
    #         for value in row:
    #             if value == 1 and row.index(value) <= number_of_values - 1:
    #                 print('t_{0} = '.format(i), row[-1])
    #             i += 1
    #         if len(list_counter) < number_of_values:
    #             [print('t_{0} = '.format(x), 0) for x in range(number_of_values - len(list_counter) + 1, number_of_values + 1)]
    #     else:
    #         break
    list_counter = []
    for row in t:
        i = 1
        for value in row:
            if value == 1 and row.index(value) <= number_of_values - 1:
                print('t_{0} = '.format(i), row[-1])
            i += 1
    print('Maximum function =', v)
    return v


main()

