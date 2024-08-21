# graveler-attempted-optimizations
An attempt to optimize ShoddyCast's original python code of rolling a 4-sided die 231 times, one billion times, while counting how many one side had rolled, stopping if one reaches 177. You can watch the original video [here](https://youtu.be/M8C8dHQE2Ro?si=3qMikyVjB-2UkWz-).

The original intent was to simulate a Graveler with paralysis, who had 54 "safe" move turns that could be interuppted by paralysis, not removing pp, and wasting the turn. The enemy requires to deplete all 160pp, and have 71 turns to knock themselves out, so 231 turns total to be "stalled". With 54 safe moves, we can cut down the needed stalled moves to 177 turns. So, paralysis needs to proc 177 times for the enemy to knock themselves out via Struggle. If any of these fail, the Graveler uses a Self-Destruct move, resulting in its, well, self-destruction.

Paralysis has a 1/4 chance of proccing, and with a need to succeed at least 177 times out of 231 gives a chance of 1 in 36 quanttourtrigintillion, or about 3.67 in 1x10^106, or one in 3 followed by 106 zeros.

This isn't happening any time soon. But it would be nice to simulate it.

ShoddyCast's original code is stored as "[graveler.py](https://github.com/Goofierknot5537/graveler-attempted-optimizations/blob/main/graveler.py)", with the total rolls changed to 100k because I don't want to wait days just to verify.

## Initial Timing
```
PS D:\Python\Graveler> python3 .\graveler.py

Took an average of 3.949372621999937 seconds
```
I used the ``timeit`` module to time the code. Put everything into a function, and ran ``timeit.timeit(rolling, number=100)`` to time it. ~4 seconds for 100k is about 25,320/sec. Faster than Austin's 1,355/sec for 1 billion in 8.5 days, but that may be due to hardware, rather than software. 

## Removal of Redundant code

There are some redundant code that we can easily remove to improve some time and readability. The ```math``` module is never used, and we can decrease items by 1 in each to remove the ```numbers[rolls-1]``` into just ```numbers[rolls]```, doing one less calculation per try. The repeat() module is efficient already, as is random.choice().
```
PS D:\Python\Graveler> python3 .\graveler1.py

Took an average of 3.8763479380001082 seconds
```
Hmmm. Not much of an improvement. Could even attribute it to random cpu flucuations, but maybe it is just a small improvement. Went up to 25,797/sec.

## Numpy

While ```random.choice()``` is pretty good, it wouldn't stand a chance against Numpy's random generator. Quick comparison in generating 100 million random numbers:
```
Random Int    = 21.86363869998604 seconds
Random Choice = 16.74171239999123 seconds
Numpy Randint = 0.596952100051567 seconds
```
So, we simply replace ```random.choice()``` with ```numpy.random.randint()```, removing the need for the ```item``` list as well. We should probably also remove the ```randint``` from the 231 for loop, as it can generate 231 nunmbers at once, and that's faster than being run 231 times. Also we can move ```numbers = [0,0,0,0]``` to the end, as it already starts at 0.
```
PS D:\Python\Graveler> python3 .\graveler2.py

Took an average of 1.7888492489990313 seconds
```
Now we're getting somewhere. This is about 55,902/sec.

## Removing loops and more Numpy

```while``` loops are slower than ```for``` loops. While having the extra comparison if the total amount of a number is less than 177 to end this early *seems* good, the chances of this happening are close to nill, and it would be faster on average just to do every roll rather than check every time if we succeeded. This removes extra operations, as well as using a faster loop, increasing speed by a bit.
```
PS D:\Python\Graveler> python3 .\graveler3.py

Took an average of 1.8421107560000383 seconds
```
...huh. Honestly I don't know why this happened. Subsequent tests give the same results, even though the theory should've been right. Weird.

Back to the drawing board.

In each loop, what we're doing is creating 231 random numbers, counting them up, counting each roll, setting the new max, and reseting the list. Well, what if we create every random number first, and then split it into 231-sized chunks before doing our operations on that? It removes part of the loop, and should be faster since we're only running the rng once, rather than n amount of times. 

You know what? Since we're already using numpy, let's also use it to count how many of each number we have! It's backend is in C, so it's like having the speed of C but in Python!
```
PS D:\Python\Graveler> python3 .\graveler3.py

Took an average of 0.22883855099906214 seconds
```
Hell yeah! 436,989/sec!

## Reduction

Turns out ```numpy.random.randint()``` isn't the fastest. ```numpy.random.generator``` is the fastest method. Had to look that up. It uses [PCG64](https://en.wikipedia.org/wiki/Permuted_congruential_generator), so it's apparently more efficient and more random.
```
PS D:\Python\Graveler> python3 .\graveler4.py

Took an average of 0.19178970200009643 seconds
```
Guess that's true. 521,404/sec.

At this point, everything was really situational. If there was anything faster that I actually understood, Google didn't know and ChatGPT wasn't telling.

So, rather than optimize further, what if we reduce the amount of tests needed to do? We are generating *four* numbers, after all. Each having a *1/4* chance of happening. So aren't we doing four simulations simultaniously?

By looking at every number's occurance, rather than just one, we effectively ran **four times** the simulations with only a little more overhead. ```bincount()``` also happens to count *every* number in the array, so only minimal changes are needed.
```
PS D:\Python\Graveler> python3 .\graveler4.py

Took an average of 0.10215682229993399 seconds
```
About 1.88x faster. 978,887/sec.

## Memory
While running some higher numbers and looking at task manager, I saw something.
```
Python     CPU  12.7%   RAM  8,404.9 MB
```
Whoops. Maybe saving 6 billion digits into a single array wasn't the best idea. If we go any larger I'll need a better laptop. And maybe use my external storage as RAM.

No, that seems too expensive. Let's try and split it into more managable pieces. Say ~1 GB at most. ```rolls = 12000000``` seems to be at around that mark, so splitting it up into 12 million-sized chunks would be acceptable. Our code will run slightly slower since we're trying to reduce memory usage, but if you can't run it at all, is it really worth it?
```
PS D:\Python\Graveler> python3 .\graveler5.py

Took an average of 0.10254251150006893 seconds
```
Better than I expected. I won't complain, though. How's the memory going?
```
Python     CPU  12.5%   RAM  1,023.7 MB
```
That's better.

...

Hey wait, what's with that low CPU?

## Multiprocessing
Multiprocessing is hard to work around. Especially if it's your first time (like me). So when I set up the code and put on 10 processors or so it ended up being slower than a lower amount! It seemed to hover around 3 cores when doing 20 million rolls. Why might this be?

After research, I still can't really narrow it down. I do have some theories, but for now I'll just experiment with optimal amounts of processors. It seems that as roll count goes up, it's optimal to use more processors, though I don't know how it correlates. There's also a sudden drop when doing 9 million rolls during some tests for whatever reason.

Here's some graphs I made to show what I mean.

![Graph1](/Graphs/Graph1.png)
![Graph2](/Graphs/Graph2.png)

Looks like 3 cores is my best bet for now. I've tried higher cores, but things just get longer. 

Anyways, how's the speed looking? I'll do 10 million instead of 100k so the cores can prepare.

```
PS D:\Python\Graveler> python3 .\graveler5.py

Took an average of 10.253912020009011 seconds
```
```
PS D:\Python\Graveler> python3 .\graveler6.py

Took an average of 6.75167722000042 seconds
```
Pretty good. 5's test is 975,237/sec, 6 is 1,481,113/sec.

## Is there more?
There are probably more optimizations to be found in this code. If the multiprocessing was fixed, the code could probably use as many cores as wanted, but I don't want to figure that out. I've spent enough time on this already. 

Profiling shows that most of our time is spent on executing ```np.max(numbers)```, ```np.argmax(numbers)```, and ```np.array_split(random,new_rolls)```. If there are more efficient options or a way to get around using these, time could possibly be improved.

Of course, we could also just forgo almost everything about this simulation and use the wisdom of another [youtuber](https://www.youtube.com/watch?v=Qgevy75co8c)...
```
import numpy as np
import timeit

rng = np.random.default_rng()
def rolls():
    numMax = 0
    random = rng.binomial(n = 231, p=0.25, size = 10000000)
    maximum = np.max(random)
    if maximum > numMax:
    numMax = np.max(random)

result = timeit.timeit(rolls, number=100)
print(f"\nTook an average of {result / 100} seconds\n")
```
```
PS D:\Python\Graveler> python3 .\graveler7.py

Took an average of 0.45558782099979 seconds
```
...don't use loops. Use math.

Unless it's for memory managment[^1].

[^1]: This is my opinion, the youtuber never said this. Please don't sue me.

## Final times
| File | Experimental Speed | Estimated Completion (1B) |
| ---- | ------------------ | ------------------------- |
| graveler.py | 25,320/sec | 10 hours, 58 minutes, 15 seconds |
| graveler1.py | 25,797/sec | 10 hours, 46 minutes, 5 seconds |
| graveler2.py | 55,902/sec | 4 hours, 58 minutes, 9 seconds |
| graveler3.py | 436,989/sec | 38 minutes, 9 seconds |
| graveler4.py | 978,887/sec | 17 minutes, 2 seconds |
| graveler5.py | 975,205/sec | 17 minutes, 6 seconds | 
| graveler6.py | 1,481,113/sec | 11 minutes, 16 seconds|
| graveler7.py | 21,949,665/sec | 45.56 seconds |

So, how much time could Austin have saved if he used these files instead of his own? My tests are 18.6863x faster than Austin's, so I'll just divide my speed by that.

If he used graveler5.py, it would've taken 5 hours, 19 minutes, 22 seconds.

For graveler6.py, 3 hours, 30 minutes, 17 seconds.

And for graveler7.py, 14 minutes, 12 seconds.

Thank you for the opportunity to optimize code, I haven't done this before so I also learned a lot of new things. I don't think I'll even touch multiprocessing again, though. Still, it was fun to do. ~~even if it took me three days to complete~~
