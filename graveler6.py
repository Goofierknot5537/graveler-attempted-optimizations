import numpy as np
import multiprocessing

rolls = 10000000
limit = 6000000
num_of_processors = 3

rng = np.random.default_rng()

def worker(maxNum, rolls):

    def rolling(rolls):
        new_rolls = -(rolls // -4)

        random = rng.integers(0,4, size=(231 * new_rolls), dtype=np.int8)

        divided_random = np.array_split(random,new_rolls)

        random = None

        for array in divided_random:
            numbers = np.bincount(array)
            localmax = np.max(numbers)
            maxpos = np.argmax(numbers)

            if localmax > maxNum[maxpos]:
                maxNum[maxpos] = localmax
                
        
        divided_random = None

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

def main():
    maxNum = multiprocessing.Array('i', 4)

    new_rolls = -(rolls // -num_of_processors)

    processes = []
    for i in range(num_of_processors):
        p = multiprocessing.Process(target=worker, args=(maxNum, new_rolls))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"Highest Roll: {max(maxNum)}\n"
          f"Number of Roll Sessions: {rolls}")

if __name__ == '__main__':
    main()