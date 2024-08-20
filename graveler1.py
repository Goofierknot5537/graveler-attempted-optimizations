import random
from itertools import repeat
import timeit

def rolling():
    items = [0,1,2,3]
    numbers = [0,0,0,0]
    rolls = 0
    maxOnes = 0

    while numbers[0] < 177 and rolls < 100000:

        numbers = [0,0,0,0]

        for i in repeat(None, 231):
            roll = random.choice(items)
            numbers[roll] += 1
        
        rolls += 1

        if numbers[0] > maxOnes:
            maxOnes = numbers[0]

result = timeit.timeit(rolling, number = 100)
print(f"\nTook an average of {result / 100} seconds\n")
