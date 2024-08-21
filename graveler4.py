import numpy as np

rolls = 100000
new_rolls = -(rolls // -4)
maxNum = [0,0,0,0]

rng = np.random.default_rng()

random = rng.integers(0,4, size=(231 * new_rolls), dtype=np.int8)

divided_random = np.array_split(random, new_rolls)

for array in divided_random:
    numbers = np.bincount(array)
    localmax = np.max(numbers)
    maxpos = np.argmax(numbers)

    if localmax > maxNum[maxpos]:
        maxNum[maxpos] = localmax

print(f"Highest Roll: {max(maxNum)}\n"
      f"Number of Roll Sessions: {rolls}")
