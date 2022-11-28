import numpy as np
from fractions import Fraction

n = int(input("Type the size of the matrix: "))

matrix = np.zeros((n, n), dtype= Fraction)
inverse = np.zeros((n, n), dtype= Fraction)

for i in range(n):
    for j in range(n):

        value = Fraction(input("Type the value of the Row: {}, Column: {}: ".format(i+1, j+1)))        
        if value % 1 != 0:
            print("\n We've detected the number you typed was a rational number, please type what is asked to you in the following gaps: ")
            numerator = int(input(" Type the numerator of your number: "))
            denominator = int(input(" Type the denominator of your number: "))
            print("")
            value = Fraction(numerator, denominator)
        
        matrix[i][j] = value


def invert(dimension, matrix):
    for i in range(dimension):
            # This fills the inverse matrix as the identity matrix and sets the value to divide each row
            divideby = matrix[i][i]
            inverse[i][i] = Fraction(1, 1)

            for j in range(dimension):

                # Now we turn each element of the diagnal into a 1
                matrix[i][j] = Fraction(matrix[i][j], divideby)
                inverse[i][j] = Fraction(inverse[i][j], divideby)

            for k in range(dimension):

                # And we operate til each element different from the one on the diagonal turns into 0
                if k != i:
                    tomultiply = matrix[k][i]
                    for l in range(dimension):
                        matrix[k][l] = matrix[k][l] - matrix[i][l]*tomultiply
                        inverse[k][l] = inverse[k][l] - inverse[i][l]*tomultiply


print(matrix)
print(inverse)


        


