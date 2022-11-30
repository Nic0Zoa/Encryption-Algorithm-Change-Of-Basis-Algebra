
import numpy as np
from fractions import Fraction

# Let's define an array we are gonna use in the process. This will correspond to an array that contains our alphabet and two things more

ALPHABET = ['_', 'A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.']


# We will use different arrays that are gonna change its state along the process, in order to keep code legible, we are gonna enumerate them all right below

# The name of the arrays is easy to understand. First Bi represents the base of the vector written below, while the name says it all.

B1_INDEXVECTOR = []
B1_STRINGVECTOR = []
B2_INDEXVECTOR = []
B2_STRINGVECTOR = []

# Now we are gonna define a couple of functions

# We need a function in order to fill our matrix
def fill_matrix(dimension, matrix, auxiliarmatrix):
    for i in range(dimension):
        for j in range(dimension):
            value = Fraction(
                input("Type the value of the Row: {}, Column: {}: ".format(i+1, j+1)))

            if value % 1 != 0:
                print("\n We've detected the number you typed was a rational number, please type what is asked to you in the following gaps: ")
                numerator = int(
                    input(" Type the numerator of your number: "))
                denominator = int(
                    input(" Type the denominator of your number: "))
                print("")
                value = Fraction(numerator, denominator)

            auxiliarmatrix[i][j] = value
            matrix[i][j] = value

# As we are working in Z_29, we turn each element of the matrix into an element of Z_29

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


# For any matrix, this function inverts the given matrix in order to get the change of basis matrix one
def invert(dimension, matrix, inverse):
    temparrayoriginal = np.zeros(dimension, dtype=Fraction)
    temparrayinverse = np.zeros(dimension, dtype=Fraction)

    for i in range(dimension):
        inverse[i][i] = Fraction(1, 1)

    for i in range(dimension):
        if matrix[i][i] == 0:
            for k in range(dimension):
                if matrix[k][i] != 0:
                    for j in range(dimension):
                        temparrayoriginal[j] = matrix[i][j]
                        temparrayinverse[j] = inverse[i][j]

                    for j in range(dimension):
                        matrix[i][j] = matrix[k][j]
                        matrix[k][j] = temparrayoriginal[j]
                        inverse[i][j] = inverse[k][j]
                        inverse[k][j] = temparrayinverse[j]
                    break
        divideby = matrix[i][i]

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
        

    # This is the most important function, as we are wokring in Z_29^3 we need, always,  the lenght of our index array to be a multiple of 3, now with this fuction, if necessary,  we fill the missing spaces

def fill_missing_spaces(dimension, indexvector):

    iterator = dimension - len(indexvector) % dimension
    if iterator != 0:
        for i in range(iterator):
            indexvector.append(0)
        for i in range(dimension):
            indexvector.pop()


    # This function takes every letter of a string and turns it into the number that it represents

def string_to_index(string, indexvector, alphabetvector):
    for i in string:
        for j in range(len(alphabetvector)):
            if i == alphabetvector[j]:
                indexvector.append(j)

    # This function turns every number from a vector of index and turns it into a letter of the alphabet

def index_to_string(indexvector, stringvector, alphabetvector):
    TEMPINDEXVECTOR = []
    for i in range(len(indexvector)):
        TEMPINDEXVECTOR.append(indexvector[i] % 29)
        stringvector.append(alphabetvector[TEMPINDEXVECTOR[i]])

    # It is important to keep our message protected, that's why we will define a couple of functions to do this.

    # Given the change of basis matrix, the next step is to multiply each Z_29^3 vector to our matrix. The first step is to define a new vector each three elements of the array of index. In other words, to create the vector that will be multiplied by the change of basis matrixr.
    
def change_of_basis_process(dimension, indexvector, changeofbasismatrix, resultingarray):

    # These vectors are temporary vectors that will help us when we take the product

    TEMPVECTORTOMULTIPLY = np.ones((dimension, 1), dtype= Fraction)
    TEMPVECTORENCRYPTED = np.ones((dimension, 1), dtype= Fraction)

    for i in range(3):
        TEMPVECTORENCRYPTED[i] = 0
        TEMPVECTORTOMULTIPLY[i] = 0

    for i in range(len(indexvector)):

        # The first part of this foor loop creates a new vector each three elements. This new vector is the one that is gonna be multiplied by the change of basis matrix

        index = i % 3
        TEMPVECTORTOMULTIPLY[index] = indexvector[i]

        if i % dimension == (dimension - 1):
            # Now we take the vector we filled before and make the product between this vector and the change of basis matrix

            TEMPVECTORENCRYPTED = np.matmul(changeofbasismatrix, TEMPVECTORTOMULTIPLY)
            
            # The last part of the process is to take each of the vector coordinates and append them into a new array. This new array represents our encrypted message.

            for i in range(dimension):
                tempvalue = TEMPVECTORENCRYPTED[i][0]
                resultingarray.append(tempvalue)


# Now this is pure aesthetics, this will just make the string vector look better
def prettify(stringarray):
    for i in range(len(stringarray)):
        if stringarray[i] == '_':
            stringarray[i] = ' '


# And we make our program interactive, we don't really need to explain this part

print("Welcome. I hope you enjoy the program, take a sit and follow my instructions.")

# First we wanna know the key to use for decrypt and encrypt our message, so we ask the user to type the size of the matrix, and each element of the matrix
n = int(input("\nType the size of the matrix (Just type the number of columns): "))

# Of course we will need the inverse of this matrix, is our way to encrypt our message, so we define these two matrix.
matrix = np.zeros((n, n), dtype= Fraction)
auxmatrix = np.zeros((n, n), dtype= Fraction)
inverse = np.zeros((n, n), dtype= Fraction)

# And we call the method to fill the principal one as we invert it
print("It's time to enter your key:")
print("")
fill_matrix(n, matrix, auxmatrix)
invert(n, auxmatrix, inverse)

# Right below you will find the two matrix that are gonna be used. The first one represent the matrix B1 to B2,in other words, our key. While the second matrix is the one we are going to use to encrypt our message

B1_B2 = np.zeros((n, n), dtype= Fraction)
B2_B1 = np.zeros((n, n), dtype= Fraction)

# We are working on Z_29, but the inverse function doesn't give a fuck about that. It may be possible that we end up with a matrix full of fractions, and we got no idea of what a fraction is in a finite field. So above, we define a function that, given any number, turn that number into an element of the field.

turntoZ29(n, matrix, B1_B2)
turntoZ29(n, inverse, B2_B1)

for i in range(n):
    for j in range(n):
        value1 = B1_B2[i][j]
        value2 = B2_B1[i][j]
        numerator1 = value2.numerator
        numerator2 = value1.numerator

        B2_B1[i][j] = numerator1
        B1_B2[i][j] = numerator2

print("\n Congratulations, we're almost done. Now the final part")



while True:

    B1_INDEXVECTOR = []
    B1_STRINGVECTOR = []
    B2_INDEXVECTOR = []
    B2_STRINGVECTOR = []
    ENCRYPTEDVECTOR = []

    string = str(input("Enter the string to process: "))


    condition = int(input(
        "\n\nIs the string written in normal language or is it encrypted. \n\n If it's written in natural language, type '1' \n If it's encrypted type '2' \n\n Your answer here: "))

    if condition == 1:

        string_to_index(string, B1_INDEXVECTOR, ALPHABET)
        fill_missing_spaces(n, B1_INDEXVECTOR)
        index_to_string(B1_INDEXVECTOR, B1_STRINGVECTOR, ALPHABET)


        change_of_basis_process(n, B1_INDEXVECTOR, B2_B1, B2_INDEXVECTOR)
        change_of_basis_process(n, B1_INDEXVECTOR, inverse, ENCRYPTEDVECTOR)

        index_to_string(B2_INDEXVECTOR, B2_STRINGVECTOR, ALPHABET)

        prettify(B1_STRINGVECTOR)

        for i in range(len(B2_INDEXVECTOR)):
            value = ENCRYPTEDVECTOR[i]
            valuenumerator = value.numerator
            valuedenominator = value.denominator
            value = valuenumerator/valuedenominator
            ENCRYPTEDVECTOR[i] = round(value, 2)


        print("\n\nThe message you typed was the following:", ''.join(B1_STRINGVECTOR))
        print("\n It can also be expressed as the following array:", B1_INDEXVECTOR)

        print("\n After a hard process of encrypting your message, the resulting string of characters is the following:", ''.join(B2_STRINGVECTOR))
        print("\n Good luck to everyone trying to decrypt this array: ", ENCRYPTEDVECTOR)

        print("\n\n")

    elif condition == 2:

        string_to_index(string, B2_INDEXVECTOR, ALPHABET)
        fill_missing_spaces(n, B2_INDEXVECTOR)

        change_of_basis_process(n, B2_INDEXVECTOR, B1_B2, B1_INDEXVECTOR)
        index_to_string(B1_INDEXVECTOR, B1_STRINGVECTOR, ALPHABET)

        prettify(B1_STRINGVECTOR)

        print("\n\nThe message you typed was the following:", ''.join(B2_STRINGVECTOR))
        print("\n After a hard process of dencrypting your message, the resulting string of characters is the following:",
            ''.join(B1_STRINGVECTOR))
        print("\n You can thank me later")

        print("\n\n")

