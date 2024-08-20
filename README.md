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
I used the ``timeit`` module to time the code. Put everything into a function, and ran ``timeit.timeit(rolling, number=100)`` to time it. ~4 seconds for 100k is about 25,320/sec. Faster than Dustin's 1,355/sec for 1 billion in 8.5 days, but that may be due to hardware, rather than software. 

## Removal of Redundant code

There are some redundant code that we can easily remove to improve some time and readability. The ```math``` module is never used, and we can decrease items by 1 in each to remove the ```numbers[rolls-1]``` into just ```numbers[rolls]```, doing one less calculation per try. The repeat() module is efficient already, as is random.choice().
```
PS D:\Python\Graveler> python3 .\graveler1.py

Took an average of 3.8763479380001082 seconds
```
Hmmm. Not much of an improvement. Could even attribute it to random cpu flucuations, but maybe it is just a small improvement. Went up to 25,797/sec. The file will be in [graveler1.py](https://github.com/Goofierknot5537/graveler-attempted-optimizations/blob/main/graveler1.py).

## Numpy

While ```random.choice()``` is pretty good, it wouldn't stand a chance against Numpy's random generator. Quick comparison in generating 100 million random numbers:
```
Random Int    = 21.86363869998604 seconds
Random Choice = 16.74171239999123 seconds
Numpy Randint = 0.596952100051567 seconds
```
So, we simply replace ```random.choice()``` with ```numpy.random.randint()```, removing the need for the ```item``` list as well. We should probably also remove it from the 231 for loop, as it can generate 231 nunmbers at once, and that's faster than being run 231 times. Also we can move ```numbers = [0,0,0,0]``` to the end, as it already starts at 0.
```
PS D:\Python\Graveler> python3 .\graveler2.py

Took an average of 1.7888492489990313 seconds
```
Now we're getting somewhere. This is about 55,902/sec.

## Removing the while loop

```while``` loops are slower than ```for``` loops. While having the extra comparison if the total amount of a number is less than 177 to end this early *seems* good, the chances of this happening are close to nil, and it would be faster on average just to do every roll rather than check every time if we succeeded. 

