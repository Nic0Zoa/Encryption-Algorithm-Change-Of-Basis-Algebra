import numpy as np
from fractions import Fraction
from decimal import Decimal


# First we turn each integer into an element of Z_29

matrix = np.array([[1, Fraction(31, 2), 2], [30, 31, 32], [-1, -2, -3]], dtype= Fraction)
matrix29 = np.ones((3, 3), dtype= Fraction)

def turntoZ29(dimension, matrix, resultingmatrix):
    for i in range(dimension):
        for j in range(dimension):
            valuetoassign = matrix[i][j]
            if valuetoassign % 1 != 0:
                fractionNumerator = valuetoassign.numerator
                fractionDenominator = valuetoassign.denominator

                a = fractionNumerator
                b = fractionDenominator
                multiplicativeinverse = 0

                while True:
                    multiplicativeinverse += 1
                    product = b*multiplicativeinverse
                    if product % 29 == 1:
                        break

                a = fractionNumerator % 29
                b = multiplicativeinverse

                valuetoassign = a*b
      
            resultingmatrix[i][j] = valuetoassign % 29    


turntoZ29(3, matrix, matrix29)
print(matrix29)
