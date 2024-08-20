import numpy.random as nprandom

numbers = [0,0,0,0]
rolls = 0
maxOnes = 0

while numbers[0] < 177 and rolls < 100000:

    random = nprandom.randint(0,3, size=231)

    for i in random:
        numbers[i] += 1
    
    rolls += 1

    if numbers[0] > maxOnes:
        maxOnes = numbers[0]

    numbers = [0,0,0,0]

print("Highest Ones Roll:",maxOnes)
print("Number of Roll Sessions: ",rolls)