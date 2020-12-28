'''
Created on Dec 27, 2020

@author: Todor Balabanov
'''

import sys
import random
import pandas
import tqdm
 
''' Lines information. '''
LINES = [[1, 1, 1, 1, 1, ],
         [0, 0, 0, 0, 0, ],
         [2, 2, 2, 2, 2, ],
         [0, 1, 2, 1, 0, ],
         [2, 1, 0, 1, 2, ],
         [1, 0, 0, 0, 1, ],
         [1, 2, 2, 2, 1, ],
         [0, 0, 1, 2, 2, ],
         [2, 2, 1, 0, 0, ],
         [1, 2, 1, 0, 1, ],
         [1, 0, 1, 2, 1, ],
         [0, 1, 1, 1, 0, ],
         [2, 1, 1, 1, 2, ],
         [0, 1, 0, 1, 0, ],
         [2, 1, 2, 1, 2, ],
         [1, 1, 0, 1, 1, ],
         [1, 1, 2, 1, 1, ],
         [0, 0, 2, 0, 0, ],
         [2, 2, 0, 2, 2, ],
         [0, 2, 2, 2, 0, ],
         [2, 0, 0, 0, 2, ],
         [1, 2, 0, 2, 1, ],
         [1, 0, 2, 0, 1, ],
         [0, 2, 0, 2, 0, ],
         [2, 0, 2, 0, 2, ], ]
 
''' Pay table information. Index 0 is a scatter. Index 1 is a wild. '''
PAYTABLE = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [1, 0, 10, 10, 10, 10, 5, 5, 5, 5, 0, 0, 0, ],
            [0, 0, 50, 50, 25, 25, 15, 15, 15, 15, 0, 0, 0, ],
            [0, 0, 500, 300, 250, 200, 100, 100, 100, 100, 0, 0, 0, ], ]
 
'''
 Shoe win probability distribution. First is value and second is the chance (sum of chances is 100).
 '''
SHOE = [5] * 17 + [10] * 16 + [15] * 16 + [25] * 16 + [50] * 15 + [100] * 10 + [200] * 5 + [250] * 3 + [300] * 2 + [500] * 1
 
'''
 Jakpot win probability distribution. First is value and second is the chance (sum of chances is 1000).
 '''
JACKPOT = [0] * 990 + [3] * 4 + [5] * 3 + [7] * 2 + [9] * 1
 
''' Names of the symbols. '''
SYMBOLS_NAMES = ["FIRE", "GOLD", "WHITE", "BLACK", "BOY", "GIRL", "ACE", "KING", "QUEEN", "JACK", "SHOE", "JACKPOT", "COLLECT"]
 
''' Text representation of the base game reels. '''
BASE_GAME_REELS_TEXT = pandas.read_csv("base.csv", header=None)
 
''' Text representation of the free spins reels. '''
FREE_SPIN_REELS_TEXT = pandas.read_csv("free.csv", header=None)
 
''' Numerical representation of the base game reels. '''
BASE_GAME_REELS = [[], [], [], [], [], ]
 
''' Numerical representation of the free spins reels. '''
FREE_SPIN_REELS = [[], [], [], [], [], ]
 
''' Probability distribution of the free spins activated in base game. '''
FREE_SPINS_IN_BASE = [0, 0, 0, 8, 0, 0]
 
''' Probability distribution of the free spins activated in free spins. '''
FREE_SPINS_IN_FREE = [0, 0, 0, 8, 0, 0]
 
''' Flag for verbose output. '''
verboseOutput = False
 
''' Print of model input data flag. '''
inDataOutput = False
 
''' Counter of the total number of games. '''
totalNumberOfGames = 0
 
''' Counter of the total number of free spins. '''
totalNumberOfFreeGames = 0
 
''' Counter of the total number of free spins starts. '''
totalNumberOfFreeStarts = 0
 
''' Counter of the total number of free spins restarts. '''
totalNumberOfFreeRestarts = 0
 
''' Counter of the total number of bonus games. '''
totalNumberOfBonusGames = 0
 
''' Total amount of won money. '''
wonMoney = 0
 
''' Total amount of lost money. '''
lostMoney = 0
 
''' Total amount of won money into base game. '''
baseMoney = 0
 
''' Total amount of won money into free spins. '''
freeMoney = 0
 
''' Total amount of won money into bonus game. '''
bonusMoney = 0
 
''' Win hit rate into base game. '''
baseGameHitRate = 0
 
''' Win hit rate into free spins. '''
freeGamesHitRate = 0
 
''' Win hit rate into free spins. '''
bonusGameHitRate = 0
 
''' Counter of the free spins during simulation run of a free spins. '''
freeGamesNumber = 0
 
''' Counter of the bonus games during simulation run of a bonus games. '''
bonusGamesNumber = 0
 
''' Total bet for a single spin of a base game. '''
totalBet = len(LINES)
 
''' Screen configuration after reels spins. '''
view = [[-1, -1, -1],
        [-1, -1, -1],
        [-1, -1, -1],
        [-1, -1, -1],
        [-1, -1, -1]]
 
'''
 Print active screen configuration.
 
 @param view
            Screen configuration as numbers.
 '''


def printView(view):
    max = len(view[0])
    for i in range(0, len(view)):
        if max < len(view[i]):
            max = len(view[i])
 
    for j in range(0, max):
        for i in range(0, min(len(view), len(view[i]))):
            print(SYMBOLS_NAMES[view[i][j]] + "\t", end="")
 
        print()

'''
 Transform text reels information into number reels information.
   
 @param numbers
            Resulting reels as numbers.
 @param text
            Reels as text.
   
 @return Reference to the array with reels as numbers.
 '''


def reelsFromTextToNumbers(numbers, text):
    ''' Fill reels structure. '''
    for i in range(0, len(text)):
        for j in range(0, len(text[i])):
            numbers[i].insert(j, -1)
            for k in range(0, len(SYMBOLS_NAMES)):
                if SYMBOLS_NAMES[k] not in text[i][j]:
                    continue
                numbers[i][j] = k
                break
   
    return numbers

  
''' Initialization of the static members. '''
reelsFromTextToNumbers(BASE_GAME_REELS, BASE_GAME_REELS_TEXT.transpose().to_numpy())
reelsFromTextToNumbers(FREE_SPIN_REELS, FREE_SPIN_REELS_TEXT.transpose().to_numpy())
 
'''
 Calculation of the win from a single line.
 
 @param line
            Line of symbols as numbers.
 
 @return Win from the line.
 '''


def lineWin(line):
    '''
     Keep first symbol in the line.
     '''
    symbol = line[0]
 
    ''' If there is no symbol there is no win. '''
    if symbol == -1:
        return 0
 
    '''
     Wild symbol passing to find first regular symbol.
     '''
    for i in range(0, len(line)):
        '''
         First no wild symbol found.
         '''
        if symbol != 1:
            break
 
        symbol = line[i]
 
    '''
     Wild symbol substitution.
     '''
    for i in range(0, len(line)):
        if line[i] == 1:
            '''
             Substitute wild with regular symbol.
             '''
            line[i] = symbol
 
    '''
      Count symbols in winning line.
     '''
    number = 0
    for i in range(0, len(line)):
        if line[i] == symbol:
            number += 1
        else:
            break
 
    '''
      Clear unused symbols.
     '''
    for i in range(number, len(line)):
        line[i] = -1
 
    win = PAYTABLE[number][symbol]
 
    return win
 
'''
 Win from all lines for particular screen configuration.
 
 @param view
            Screen configuration as numbers.
 
 @return Total win of lines.
 '''


def linesWin(view):
    win = 0
 
    '''
     Check wins in all possible lines.
     '''
    for l in range(0, len(LINES)):
        line = [-1, -1, -1, -1, -1]
 
        '''
         Prepare line for combination check.
         '''
        for i in range(0, len(line)):
            index = LINES[l][i]
            line[i] = view[i][index]
 
        result = lineWin(line)
 
        '''
         Accumulate line win.
         '''
        win += result
 
    return (win)
 
'''
 Win of scatters on the particular screen configuration.
 
 @param view
            Screen configuration.
 
 @return Total win of scatters.
 '''


def scattersWin(view):
    number = 0
 
    for i in range(0, len(view)):
        for j in range(0, len(view[i])):
            if view[i][j] != 0:
                continue
 
            number += 1
 
    ''' Scatter is on index 0. '''
    return (PAYTABLE[number][0] * totalBet)

'''
 Win of horse shoe from the rules of Mustang Gold.
   
 @return Total win of horse shoe.
 '''


def collectWin():
    win = 0
    collect = 0
  
    for i in range(0, len(view)):
        for j in range(0, len(view[i])):
            '''
             Win is collected only if the collect symbol is on the screen.
             '''
            if view[i][j] == 12:
                collect = 1
  
            ''' Only shoe symbols accumulate such a win. '''
            if view[i][j] != 10:
                continue
  
            win += random.choice(SHOE)
  
    return win * collect
 
'''
 Single spin of the reels.
  
 @param view
            Screen configuration.
 @param reels
            Particular reels.
 '''


def spin(view, reels):
    for i in range(0, min(len(view), len(reels))):
        r = random.randint(0, len(reels[i]) - 1)
        u = r - 1
        d = r + 1
 
        if u < 0:
            u = len(reels[i]) - 1
 
        if d >= len(reels[i]):
            d = 0
 
        view[i][0] = reels[i][u]
        view[i][1] = reels[i][r]
        view[i][2] = reels[i][d]
 
'''
 Calculation of the free spins number.
  
 @param freeSpins
            Free spins discrete probability distribution.
  
 @return Number of free spins to play.
 '''


def numberOfFreeSpins(freeSpins):
    number = 0
    for i in range(0, len(view)):
        for j in range(0, len(view[i])):
            if view[i][j] != 0:
                continue
            number += 1
 
    return (freeSpins[number])
 
'''
 Run bonus game condition check.
  
 @return True if bonus game should run, false otherwise.
 '''


def numberOfBonusGames():
    collect = False
    jackpot = 0
 
    for i in range(0, len(view)):
        for j in range(0, len(view[i])):
            '''
             Bonus game is activated only if the collect symbol is on the
             screen.
             '''
            if view[i][j] == 12:
                collect = True
 
            ''' Only shoe jackpot symbols activate bonus game. '''
            if view[i][j] != 11:
                jackpot += 1
 
    if collect == False:
        jackpot = 0
 
    return jackpot
 
'''
 Run of a single bonus game.
 '''


def singleBonusGame():
    counters = {}
   
    ''' Initialize zeros for a histogram. '''
    for i in range(0, len(JACKPOT)):
        counters[JACKPOT[i]] = 0
    
    for i in range(0, len(view)):
        for j in range(0, len(view[i])):
            value = random.choice(JACKPOT)
            counters[value] = counters[value] + 1
    
    win = 0
    for i in range(0, len(JACKPOT)):
        ''' Only 3 or more rise a win. '''
        if counters[JACKPOT[i]] < 3 or JACKPOT[i] == 0:
            continue
        win = JACKPOT[i] * totalBet
        break
    
    '''
     Add win to the statistics.
     '''
    global bonusMoney
    bonusMoney += win
    global wonMoney
    wonMoney += win
    
    global bonusGameHitRate
    if win > 0:
        '''
         Count free spins hit rate.
         '''
        bonusGameHitRate += 1
 
'''
 Run of a single free spin.
 '''


def singleFreeGame():
    spin(view, FREE_SPIN_REELS)
  
    win = linesWin(view) + scattersWin(view) + collectWin()
  
    '''
     Add win to the statistics.
     '''
    global freeMoney
    freeMoney += win
    global wonMoney
    wonMoney += win
  
    '''
     Count free spins hit rate.
     '''
    global freeGamesHitRate
    if win > 0:
        freeGamesHitRate += 1
  
    value = numberOfFreeSpins(FREE_SPINS_IN_FREE)
  
    '''
     Count how many times free games are re-triggered.
     '''
    global totalNumberOfFreeRestarts
    if value > 0:
        totalNumberOfFreeRestarts += 1
  
    '''
     Number of free games should be added.
     '''
    global freeGamesNumber
    freeGamesNumber += value
    
    '''
     Number of bonus games should be added.
     '''
    global bonusGamesNumber
    bonusGamesNumber += numberOfBonusGames()
  
    '''
     Play bonus game if any.
     '''
    global totalNumberOfBonusGames
    for g in range(0, bonusGamesNumber):
        totalNumberOfBonusGames += 1
        singleBonusGame()
 
'''
 Run of a single base game.
 '''


def singleBaseGame():
    spin(view, BASE_GAME_REELS)
  
    win = linesWin(view) + scattersWin(view) + collectWin()
  
    '''
     Add win to the statistics.
     '''
    global baseMoney
    baseMoney += win
    global wonMoney
    wonMoney += win
  
    '''
     Count base game hit rate.
     '''
    global baseGameHitRate
    if win > 0:
        baseGameHitRate += 1
  
    '''
     Number of free games should be added.
     '''
    global freeGamesNumber
    freeGamesNumber += numberOfFreeSpins(FREE_SPINS_IN_BASE)
    
    '''
     Number of bonus games should be added.
     '''
    global bonusGamesNumber
    bonusGamesNumber += numberOfBonusGames()

    '''
     Count number of into free games.
     '''
    global totalNumberOfFreeStarts
    if freeGamesNumber > 0:
        totalNumberOfFreeStarts += 1
  
    '''
     Play all triggered free games.
     '''
    global totalNumberOfFreeGames
    for g in range(0, freeGamesNumber):
        totalNumberOfFreeGames += 1
        singleFreeGame()
  
    freeGamesNumber = 0
  
    '''
     Play bonus game if any.
     '''
    global totalNumberOfBonusGames
    for g in range(0, bonusGamesNumber):
        totalNumberOfBonusGames += 1
        singleBonusGame()
 
'''
 Print all input data for cross-check of the model.
 '''


def printDataStructures():
    if inDataOutput == False:
        return
 
    print("================================================================================")
    print("================================================================================")
    print("================================================================================")
 
    print("Paytable:")
    for i in range(0, len(PAYTABLE)):
        print("\t" + i + " of", end="")
    print()
    for j in range(0, len(PAYTABLE[0])):
        print("SYM" + j + "\t", end="")
        for i in range(0, len(PAYTABLE)):
            print(PAYTABLE[i][j] + "\t", end="")
        print()
    print()
 
    print("Scatters:")
    print("Number\tFree Games in Base Game")
    for i in range(0, len(FREE_SPINS_IN_BASE)):
        print(i + "\t" + FREE_SPINS_IN_BASE[i])
    print()
    print("Number\tFree Games in Free Spins")
    for i in range(0, len(FREE_SPINS_IN_FREE)):
        print(i + "\t" + FREE_SPINS_IN_FREE[i])
    print()
 
    print("Lines:")
    for i in range(0, len(LINES)):
        for j in range(0, len(LINES[0])):
            print(LINES[i][j] + " ", end="")
        print()
    print()
 
    print("Base Game Reels:")
    for i in range(0, len(BASE_GAME_REELS)):
        for j in range(0, len(BASE_GAME_REELS[i])):
            if j % 10 == 0:
                print()
            print("SYM" + BASE_GAME_REELS[i][j] + " ", end="")
        print()
    print()
 
    print("Free Spins Reels:")
    for i in range(0, len(FREE_SPIN_REELS)):
        for j in range(0, len(FREE_SPIN_REELS[i])):
            if j % 10 == 0:
                print()
            print("SYM" + FREE_SPIN_REELS[i][j] + " ", end="")
        print()
    print()
 
    print("Base Game Reels:")
    ''' Count symbols in reels. ''' 
    counters = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ], ]
    for i in range(0, len(BASE_GAME_REELS)):
        for j in range(0, len(BASE_GAME_REELS[i])):
            counters[i][BASE_GAME_REELS[i][j]] += 1
    for i in range(0, len(BASE_GAME_REELS)):
        print("\tReel " + (i + 1), end="")
    print()
    for j in range(0, len(counters[0])):
        print("SYM" + j + "\t", end="")
        for i in range(0, len(counters)):
            print(counters[i][j] + "\t", end="")
        print()
    print("---------------------------------------------")
    print("Total:\t", end="")
    combinations = 1
    for i in range(0, len(counters)):
        sum = 0
        for j in range(0, len(counters[0])):
            sum += counters[i][j]
        print(sum + "\t", end="")
        if sum != 0:
            combinations *= sum
    print()
    print("---------------------------------------------")
    print("Combinations:\t" + combinations)
    print()
 
    print("Free Spin Reels:")
    ''' Count symbols in reels. '''
    counters = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ], ]
    for i in range(0, len(FREE_SPIN_REELS)):
        for j in range(0, len(FREE_SPIN_REELS[i])):
            counters[i][FREE_SPIN_REELS[i][j]] += 1
    for i in range(0, len(FREE_SPIN_REELS)):
        print("\tReel " + (i + 1), end="")
    print()
    for j in range(0, len(counters[0])):
        print("SYM" + j + "\t", end="")
        for i in range(0, len(counters)):
            print(counters[i][j] + "\t", end="")
        print()
    print("---------------------------------------------")
    print("Total:\t", end="")
    combinations = 1
    for i in range(i, len(counters)):
        sum = 0
        for j in range(0, len(counters[0])):
            sum += counters[i][j]
        print(sum + "\t", end="")
        if sum != 0:
            combinations *= sum
    print()
    print("---------------------------------------------")
    print("Combinations:\t" + combinations)
    print()

'''
Print of the collected statistics.
 '''


def printStatistics():
    print("Won money:\t" + str(wonMoney))
    print("Lost money:\t" + str(lostMoney))
    print("Total Number of Games:\t" + str(totalNumberOfGames))
    print()
 
    print("Total RTP:\t" + str(wonMoney / max(1, lostMoney)))
    print("Base Game RTP:\t" + str(baseMoney / max(1, lostMoney)))
    print("Free Spins RTP:\t" + str(freeMoney / max(1, lostMoney)))
    print("Bonus Game RTP:\t" + str(bonusMoney / max(1, lostMoney)))
    print()
 
    print("Base Game Hit Rate:\t" + str(baseGameHitRate / max(1, totalNumberOfGames)))
    print("Free Spins Hit Rate:\t" + str(freeGamesHitRate / max(1, totalNumberOfFreeGames)))
    print("Bonus Game Hit Rate:\t" + str(bonusGameHitRate / max(1, totalNumberOfBonusGames)))
    print()
 
    print("Hit Frequency into Free Spins:\t" + str(totalNumberOfFreeStarts / max(1, totalNumberOfGames)))
    print("Free Spins Retrigger Frequency:\t" + str(totalNumberOfFreeRestarts / max(1, totalNumberOfFreeGames)))
 
'''
Print of the help information.
'''


def printHelp():
    print("*******************************************************************************")
    print("* Mustang Gold Simulator v1.0                                                 *")
    print("* Copyrights (C) 2020 Velbazhd Software LLC ( http://veldsoft.eu/ )           *")
    print("*                                                                             *")
    print("* developed by Todor Balabanov ( todor.balabanov@gmail.com )                  *")
    print("* Sofia, Bulgaria                                                             *")
    print("*                                                                             *")
    print("* This is private property software. In-house use only.                       *")
    print("*******************************************************************************")
    print("*                                                                             *")
    print("* -h              Help screen.                                                *")
    print("* -help           Help screen.                                                *")
    print("*                                                                             *")
    print("* -l<number>      Number of games.                                            *")
    print("*                                                                             *")
    print("* -indata         Print input data structures.                                *")
    print("* -verbose        More details on simulation progress.                        *")
    print("*                                                                             *")
    print("*                                                                             *")
    print("* Output will be on the screen!                                               *")
    print("*                                                                             *")
    print("* Ctrl+C to abort simulation.                                                 *")
    print("*                                                                             *")
    print("* python Main.py -l1000                                                       *")
    print("* Do 1 000 iterations.                                                        *")
    print("*                                                                             *")
    print("* python Main.py -l1000k                                                      *")
    print("* Do 1 000 000 iterations.                                                    *")
    print("*                                                                             *")
    print("* python Main.py -l10m                                                        *")
    print("* Do 10 000 000 iterations.                                                   *")
    print("*                                                                             *")
    print("* python Main.py                                                              *")
    print("* Do 10 000 000 iterations as default value.                                  *")
    print("*                                                                             *")
    print("*******************************************************************************")
 
'''
 Print of the execution command.
 
 @param args
            Command line arguments.
 '''


def printExecuteCommand(args):
    print("Execute command:")
    print()
    
    for i in range(0, len(args)):
        print(args[i] + " ", end="")
    
    print()

'''
 Application single entry point.
 
 @param args
            Command line arguments.
'''
if __name__ == '__main__':
    random.seed()
    
    printHelp()
    print()
  
    printExecuteCommand(sys.argv)
    print()
  
    numberOfSimulations = 10000000
  
    for a in range(0, len(sys.argv)):
        if len(sys.argv) > 0 and "-l" in sys.argv[a]:
            lParameter = sys.argv[a][2:]
  
            if "k" in lParameter:
                lParameter = lParameter[0 : len(lParameter) - 1]
                lParameter += "000"
  
            if "m" in lParameter:
                lParameter = lParameter[0 : len(lParameter) - 1]
                lParameter += "000000"
  
            numberOfSimulations = int(lParameter)
  
        if len(sys.argv) > 0 and "-verbose" in sys.argv[a]:
            verboseOutput = True
  
        if len(sys.argv) > 0 and "-indata" in sys.argv[a]:
            inDataOutput = True
  
        if len(sys.argv) > 0 and "-help" in sys.argv[a]:
            exit(0)
  
        if len(sys.argv) > 0 and "-h" in sys.argv[a]:
            exit(0)
  
    for g in (range(0, numberOfSimulations)):
        if verboseOutput == True and ((g + 1) * 100) % numberOfSimulations == 0:
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print("================================================================================")
            print("Progress: " + str((10000 * (g + 1) / numberOfSimulations) / 100.0) + "%")
            print("================================================================================")
            print()
            printStatistics()
            print()
  
        totalNumberOfGames += 1
        lostMoney += totalBet
        singleBaseGame()
  
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    printDataStructures()
    print("================================================================================")
    print("================================================================================")
    print("================================================================================")
    printStatistics()
    print("================================================================================")
    print("================================================================================")
    print("================================================================================")
