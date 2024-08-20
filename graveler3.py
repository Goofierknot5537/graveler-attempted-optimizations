import numpy as np

rolls = 100000
maxOnes = 0

random = np.random.randint(0,4, size=(231 * rolls))

divided_random = np.array_split(random, rolls)

for array in divided_random:
    numbers = np.bincount(array)
    if numbers[0] > maxOnes:
        maxOnes = numbers[0]

print("Highest Ones Roll:",maxOnes)
print("Number of Roll Sessions: ",rolls)
