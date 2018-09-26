#The classic monty Hall problem is a statistics question that has puzzled the greatest statisticians.
#The purpose of this program is to prove the solution to that question via repeated simulations.
#The question is: Given three doors to choose from, one containing the prize and two containing goats, you chose a door at random, 1/3 chance of success.
#Before determining if your guess was correct, one door you did not select is revealed to contain a goat.
#You now have the opportunity to stay with your current pick, or choose the other unrevealed door.
#The correct answer is to choose the other door, as it is now a higher chance of selecting the prize.
#Originally, you had 1/3 chance of having selected the prize, and 2/3 of having selected the goat.
#When a door was revealed, showing one of the goats, the variables at play changed, making one of the two unopened doors have the prize behind it.
#By staying with your original choice, you remain at your initial odds of winning, 1/3.
#By switching, you now have a 2/3 chance of winning.
#Reason being, originally the odds were 1/3 prize, 2/3 goats.
#If you stay with your inital guess, you stay with the initial odds.
#However, after the host reveals a door, it is in your benefit to switch because if your first guess was incorrect, the more likely outcome of two thirds, switching results in a win.
#If your first guess was correct, well then you switch to a goat and are very sad.
#However, this will only happen about 1/3 of the time.
#Sound like BS? You're not alone, lets test it below to see if it's proves true over many simulations.

import multiprocessing
import random
from random import shuffle
import sys

#Most sus function, w/e it does the job
def openDoor(firstChoice, revealedDoor, doors, swap, resultQueue):
    if(swap == 0):
        if(doors[firstChoice] == 1):
            try:
                resultQueue.put(0)
            except Exception as e: print(e)
            print("Staying wins!")
            return
        print("Staying fails!")
        return
    secondChoice = [door for door in [0, 1, 2] if door not in (firstChoice, revealedDoor)]
    if(doors[secondChoice[0]] == 1):
        try:
            resultQueue.put(0)
        except Exception as e: print(e)
        print("Swapping wins!")
        return
    print("Swapping fails!")
    return

#Must reveal a non-prize door, or a 0
def hostReveal(doors, firstChoice):
    while(True):
        door = random.randint(0,2)
        if (doors[door] == 0 and door != firstChoice): return door


def runTrial(swap, resultQueue):
    #Generate doors
    doors = [0,0,1]
    shuffle(doors)

    #Select one at random
    firstChoice = random.randint(0, 2)

    #Reveal a non-prize door
    revealedDoor = hostReveal(doors, firstChoice)

    #Open a door!
    openDoor(firstChoice, revealedDoor, doors, swap, resultQueue)

#Lazy, unsafe cli evaluations
N = int(sys.argv[1])
P = int(sys.argv[2])

#Instantiate our pool rules. No running! Lol
pool = multiprocessing.Pool(processes=P)

#Queue must be ran with a manager for between process communication, or else we won't get any of the results.
stayMan = multiprocessing.Manager()
#Use said manager to make a Queue yeet
stayResults= stayMan.Queue()
stayTrials = []
#spawn those lil' fellas
for trial in range(N):
    r1 = pool.apply_async(runTrial, args=(0, stayResults))

#Do the same but for trials where we swap
swapTrials = []
swapMan = multiprocessing.Manager()
swapResults= swapMan.Queue()
for trial in range(N):
    r2 = pool.apply_async(runTrial, args=(1, swapResults))

#Bring her around cap'n
pool.close()
print("Pool closed for additional threads/changes.")
pool.join()
print("Threads returned to master process. Generating results...")

#Queues are acting weird, I could only extract values this way, please review
stayWins = 0
if stayResults.empty() == False:
    for result in iter(stayResults.get, None):
        stayWins = stayWins + 1
        if stayResults.empty(): break

swapWins = 0
if swapResults.empty() == False:
    for result in iter(swapResults.get, None):
        swapWins = swapWins + 1
        if swapResults.empty(): break

#Output results
print("{}You simulated {} trials of the monty hall problem.").format("\n\n", N)
print("By staying you won {0:.2f} percent of the time.").format((stayWins / float(N)) * float(100))
print("By swapping you won {0:.2f} percent of the time.").format((swapWins / float(N)) * float(100))
