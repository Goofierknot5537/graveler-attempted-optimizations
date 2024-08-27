# Addendum
This is mainly a place for my thoughts that I didn't think should be in the main README.md file. Reading this is not necessary, unless you want to do a psychological evaluation on who I am, or if you're just interested in what I may be writing about in here.

## Pure Python
Most of these files relys on numpy to boost up it's speed, but now that it's just choosing based on a weighted probability, and finding the max, can't we just use python itself, without importing any dirty, heinous, impure third-party libraries?

We can. It's a bit slower, though.
```python
import random as rd
from timeit import timeit

amount = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ...] #etc
prob = [1.377691070325179e-29, 1.0608221241503985e-27, 4.066484809243174e-26, ...] #etc

rolls = 1_000_000_000

sub_rolls = -(rolls // -10_000_000)

def rolling():
    maxNum = 0
    for i in range(sub_rolls):
        random = rd.choices(amount, k= -(rolls // -sub_rolls), weights=prob)
        maximum = max(random)
        if maxNum < maximum:
            maxNum = maximum
    print(f"Highest Roll: {maxNum}\n"
          f"Number of Roll Sessions: {rolls}")
print(f"Took {timeit(rolling, number=1)} seconds")
```
```
Highest Roll: 101
Number of Roll Sessions: 1000000000
Took 116.44828399999824 seconds
```
Just about four times slower. Multiprocessing leads to about the same thing, 16.76222 seconds.

## Probability generation
> Hey wait, didn't you make all those probabilties beforehand? You're not counting all that work into the time!
>
> -Theoretical person

Well, why didn't you say so sooner, theoretical person, I could do that as well! We'll have to use a different library, SciPy. The only thing we need to use in that library is the binomial formula, specifically that pmf: ```scipy.stats.binom.pmf```
```python
import numpy as np
from scipy.stats import binom
from timeit import timeit

rng = np.random.default_rng()
amount = list(range(232))
prob = [binom.pmf(k, 231, 0.25) for k in amount]

rolls = 1_000_000_000

sub_rolls = -(rolls // -10_000_000)

def rolling():
    maxNum = 0
    for i in range(sub_rolls):
        random = rng.choice(amount, -(rolls // -sub_rolls), p=prob)
        maximum = np.max(random)
        if maxNum < maximum:
            maxNum = maximum
    print(f"Highest Roll: {maxNum}\n"
          f"Number of Roll Sessions: {rolls}")
print(f"Took {timeit(rolling, number=1)} seconds")
```
Quick and easy, saves a ton of space as well. And the time?
```
Highest Roll: 100
Number of Roll Sessions: 1000000000
Took 30.321514399998705 seconds
```
As quick as ever.

