import requests
import random
from colorama import Fore
from spellchecker import SpellChecker

guessesleft = 6
target = ""

row = {
    "default":"-----",
    0:"",
    1:"",
    2:"",
    3:"",
    4:"",
    5:""
}

def reset():
    global row, target, guessesleft
    guessesleft = 6
    target = ""
    row = {
        "default":"-----",
        0:"",
        1:"",
        2:"",
        3:"",
        4:"",
        5:""
    }

def start():
    q = input("New game? (y/n)\n")
    if q.lower() == 'y':
        newgame()
    elif q.lower() == 'n':
        pass
    else:
        print("Invalid input.")
        start()

def newgame():
    global target
    reset()
    target = getword()
    guess("")

def getword():
    word = random.choice([word for word in requests.get("https://www.mit.edu/~ecprice/wordlist.10000").text.splitlines() if len(word) == 5])
    return word

def guess(invalid):
    global row
    global target
    global guessesleft
    print("\n--- WORDLE GAME ---")
    print(" ")
    for x in range(6):
        if row[x] == "":
            print(row['default'])
        else:
            print(row[x])

    if guessesleft == 0:
        end(False)
    else:
        inputguess = input(f'{invalid}Guess ({guessesleft} guesses left):  ')
        if len(inputguess) != 5:
            guess("Word too long or too short. ")
        elif (inputguess != SpellChecker().correction(inputguess)) and (inputguess not in open('wordlewords').read().splitlines()):
            guess("Invalid guess. ")
        else:
            row[6-guessesleft] = checkword(inputguess.lower())
            guessesleft -= 1
            guess("")
            
def checkword(x):
    global target 
    guessword = list(x)
    targetword = list(target)
    targ = [""]*5
    
    mig = []
    mit = []
    
    for y in range(5):
        if x == target:
            end(True)
            break
        elif guessword[y] == targetword[y]:
            targ[y] = Fore.GREEN + guessword[y]
            targetword[y] = ''
            mig.append(y)
            mit.append(y)
            
    for y in range(5):
        if y not in mig:
            for z in range(5):
                if z not in mit and guessword[y] == targetword[z]:
                    targ[y] = Fore.RED + guessword[y]
                    mig.append(y)
                    mit.append(z)
                    break
            
    for y in range(5):
        if targ[y] == "":
            targ[y] = Fore.WHITE + guessword[y]
            
    return "".join(targ) + Fore.WHITE

def end(bl):
    if bl == True:
        print(f'\nCongratulations, you win! Your word was {Fore.GREEN + target + Fore.WHITE}!')
    else:
        print(f'\nBetter luck next time :c Your word was {Fore.GREEN + target + Fore.WHITE}!')
    start()
    
start()
