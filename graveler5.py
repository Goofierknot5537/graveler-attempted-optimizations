import numpy as np

rolls = 100000
maxNum = [0,0,0,0]
limit = 12000

def rolling(rolls):
    new_rolls = -(rolls // -4)

    rng = np.random.default_rng()

    random = rng.integers(0,4, size=(231 * new_rolls), dtype=np.int8)

    divided_random = np.array_split(random,new_rolls)

    random = 0

    for array in divided_random:
        numbers = np.bincount(array)
        localmax = np.max(numbers)
        maxpos = np.argmax(numbers)

        if localmax > maxNum[maxpos]:
            maxNum[maxpos] = localmax
    
    divided_random = 0

if rolls > limit:
    chunks = rolls // limit
    remainder = rolls % limit
    repeat_list = [limit] * chunks

    if remainder > 0:
        repeat_list.append(remainder)
    
    for num in repeat_list:
        rolling(num)  
else:
    rolling(rolls)

print(f"Highest Roll: {max(maxNum)}\n"
      f"Number of Roll Sessions: {rolls}")
