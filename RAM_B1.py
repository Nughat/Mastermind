import random
from scsa import *
from player import Player

class RAM(Player):
    
    def __init__(self):

        self.player_name = "RAM"
        
    #B1 strategy that works only for a 4 6 board. It yields very few wins because it is unable to make guesses past ACED.
    #A 4 6 board would require at 1296 guesses in order to make every possible guess AAAA-FFFF, so a limit of 100 guesses
    #severely limits the sucess of this algorithm. The guess limit also means that there isn't a point in changing the 
    #first position, which can only ever be A, hence ethe exclusion of a fourthnum variable.
    
    #global vars
    num = 1
    secnum = 1
    thirdnum = 1
    prevguess = ""

    def make_guess(self, board_length, colors, scsa, last_response): 

        if (last_response[2] == 0):   #reset globals 
            color = colors[0]         #Take first color
            guess = list_to_str(color*board_length)   #Make first gues Color1 repeating board len times

            self.secnum = 1           #reset secnum
            self.thirdnum = 1       #reset thirdnum
            self.prevguess = ""        #reset prevguess

        else:
            self.prevguess = list(self.prevguess)   #convert last guess into a list so colors can be changed

            if self.num > (len(colors)-1):                        #if the last position has reached F
                self.num = 0                        #reset it to A
                self.prevguess[2] = colors[self.secnum]  #change the position before it to the next color
                self.secnum = self.secnum + 1       #increment secnum

            if self.secnum > (len(colors)-1):                     #if secnum has reached F
                self.secnum = 0                     #reset it to A
                self.prevguess[1] = colors[self.thirdnum]  #change the position before it to the next color
                self.thirdnum = self.thirdnum + 1     #increment thirdnum

            self.prevguess[3] = colors[self.num]     #set the color of the last position
            guess = list_to_str(self.prevguess)      #convert prevguess into a str and guess
            self.num = self.num + 1                  #increment the last position

        self.prevguess = guess                       #set prevguess to (current) guess
        #print(guess, " ", last_response)
        return guess                                 #return (current) guess