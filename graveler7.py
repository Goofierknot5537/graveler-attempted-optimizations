import numpy as np

rng = np.random.default_rng()

rolls = 10000000

sub_rolls = -(rolls // -10000000)

maxNum = 0
for i in range(sub_rolls):
    random = rng.binomial(n=231, p=0.25, size= -(rolls // -sub_rolls))
    maximum = np.max(random)
    if maximum > maxNum:
        maxNum = maximum

print(f"Highest Roll: {maxNum}\n"
      f"Number of Roll Sessions: {rolls}")
