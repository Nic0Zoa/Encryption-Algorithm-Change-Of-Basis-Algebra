import numpy as np
from fractions import Fraction

number = Fraction(input())

if number % 1 != 0:
    num = int(input())
    den = int(input())
    number = Fraction(num, den)

print(number)
