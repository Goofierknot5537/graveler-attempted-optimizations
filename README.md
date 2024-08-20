# graveler-attempted-optimizations
An attempt to optimize ShoddyCast's original python code of rolling a 4-sided die 231 times, one billion times, while counting how many one side had rolled, stopping if one reaches 177. You can watch the original video [here](https://youtu.be/M8C8dHQE2Ro?si=3qMikyVjB-2UkWz-).

The original intent was to simulate a Graveler with paralysis, who had 54 "safe" move turns that could be interuppted by paralysis, not removing pp, and wasting the turn. The enemy requires to deplete all 160pp, and have 71 turns to knock themselves out, so 231 turns total to be "stalled". With 54 safe moves, we can cut down the needed stalled moves to 177 turns. So, paralysis needs to proc 177 times for the enemy to knock themselves out via Struggle. If any of these fail, the Graveler uses a Self-Destruct move, resulting in its, well, self-destruction.

Paralysis has a 1/4 chance of proccing, and with a need to succeed at least 177 times out of 231 gives a chance of 1 in 36 quanttourtrigintillion, or about 3.67 in 1x10^106, or one in 3 followed by 106 zeros.

This isn't happening any time soon. But it would be nice to simulate it.

ShoddyCast's original code is stored as "[graveler.py](https://github.com/Goofierknot5537/graveler-attempted-optimizations/blob/main/graveler.py)", with the total rolls changed to 5 million because I don't want to wait 8 1/2 days just to verify.
