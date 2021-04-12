# File contains implementations for the players for Mastermind
# See main.py or examples.ipynb for example usages

import random
from scsa import *

class Player:
    """Player for Mastermind
    """

    def __init__(self):
        """Constructor for Player
        """

        self.player_name = ""

    def make_guess(self, board_length, colors, scsa, last_response):
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list of chr): Colors that could be used in the secret code.
            scsa (SCSA): SCSA used to generate secret code.
            last_response (tuple of ints): First element in tuple is the number of pegs that match exactly with the secret 
                                           code for the previous guess and the second element is the number of pegs that are 
                                           the right color, but in the wrong location for the previous guess.

        Raises:
            NotImplementedError: Function must be implemented by children classes.
        """

        raise NotImplementedError


class RandomFolks(Player):
    """Mastermind Player that makes random guesses
    """

    def __init__(self):
        """Constructor for RandomFolks
        """

        self.player_name = "RandomFolks"

    def make_guess(self, board_length, colors, scsa, last_response):
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list of chrs): Colors that could be used in the secret code.
            scsa (SCSA): SCSA used to generate secret code.
            last_response (tuple of ints): First element in tuple is the number of pegs that match exactly with the secret 
                                           code for the previous guess and the second element is the number of pegs that are 
                                           the right color, but in the wrong location for the previous guess.

        Returns:
            str: Returns guess
        """

        scsa = InsertColors()

        guess = scsa.generate_codes(board_length, colors)

        return guess


class Boring(Player):
    """Mastermind Player that guesses all the same color and chooses that color at random
    """

    def __init__(self):
        """Constructor for Boring
        """

        self.player_name = "Boring"

    def make_guess(self, board_length, colors, scsa, last_response):
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list of chrs): All possible colors that can be used to generate a code.
            scsa (SCSA): SCSA used to generate secret code.
            last_response (tuple of ints): First element in tuple is the number of pegs that match exactly with the secret 
                                           code for the previous guess and the second element is the number of pegs that are 
                                           the right color, but in the wrong location for the previous guess.

        Returns:
            str: Returns guess
        """

        color = random.sample(colors, k = 1)

        guess = list_to_str(color*board_length)

        return guess
    
class RAM(Player):
    
    def __init__(self):

        self.player_name = "RAM"
    #globals
    guessnum = 0 #to find 1st color
    guessecondnum = 0 #to find 2nd color based on the 1st color
    guesses = [] #to store all guesses
    prevGuesses = []        # Holds all guesses attempted
    responses = []          # Holds all responses corresponding to previous guesses  
    positions = {}          # Holds position data in dictionary {position: character}

    
    def make_guess(self, board_length, colors, scsa, last_response):
#_________________________________________ Two Color Alternating _________________________________________________        
        if scsa.name == "TwoColorAlternating":
            
            if (last_response[2] == 0):       #reset global vars once a new round has started
                self.guessnum = 0
                self.guessecondnum = 0
                self.guesses = []
            if not self.guesses:              #try AAAA on the first guess
                color = colors[self.guessnum] #guessnum has value 0
                guess = list_to_str(color*board_length) #guess will be the 0th element of colors, which is A
            if (self.guesses):                                           #If guesses have been made 
                if (last_response[0] == 0 and last_response[1]== 0):    #0 pegs match exactly and there were no right colors guessed
                    self.guessnum = self.guessnum+1                      #increment guessnum, try the next color in colors
                    self.guessecondnum = self.guessnum                   #update the var for the second color as well, since both colors will be found lexicographically (ex: BBBB has some correct colors, then the second color must be one that comes after B)    
                    color = colors[self.guessnum]                        #get the color of index guessnum
                    guess = list_to_str(color*board_length)             #And make a guess from it by repeating color board_length times
                elif (last_response[0] == 2):                            #2 colors in correct position
                    color = [colors[self.guessnum],colors[self.guessecondnum+1],colors[self.guessnum],colors[self.guessecondnum+1]] #assume that the colors in the correct position are the 0th and 2nd colors, so change the 1st and 3rd elements
                    guess = list_to_str(color)                     
                    self.guessecondnum = self.guessecondnum+1            #change the second color alphabetically until it is found 
                elif (last_response[0] == 0 and (last_response[1] == 4 or last_response[1] == 2)): #the assumption from the last condition causes all colors to be in wrong position, meaning that the 1st and 3rd colors were in the correct position and the 0th and 2nd elements needed to be changed   
                    color = self.guesses[-1]                             #by now, all colors are correct so just retrieve the previous guess
                    color.reverse()                                    #reverse the previous guess
                    guess = list_to_str(color)                          

            #print(guess, " ", last_response)
            self.guesses.append(color)          #store all guesses in a list in case they are needed later on
            return guess #return the guess
#_____________________________________________________ First Last _______________________________________________________
        if scsa.name == "FirstLast":
            guess = []
            missingPositions = []

            if last_response:
                self.responses.append(last_response)

            if last_response[2] == 0:
                self.prevGuesses = []
                self.responses = [last_response]
                self.positions = {}

            if last_response[0] == board_length:
                guess = self.prevGuesses[-1]
                return guess

            # Throws first guess consisting of first color * board_length (i.e. if colors[0] == A with board size 4, then returns "AAAA")
            if not self.prevGuesses:
                guess = [colors[0] for i in range(board_length)]
                self.prevGuesses.append(list_to_str(guess))
                return guess
            else:
                guess = list(self.prevGuesses[-1])

            # Fills up the positions dictionary depending on previous responses and changes
            if (last_response[0] == board_length - 1 and 0 not in self.positions) or (len(self.prevGuesses) > 1 and self.responses[-2][0] + 2 == last_response[0] and self.prevGuesses[-2] != self.prevGuesses[-1]):
                self.positions[0] = self.prevGuesses[-1][0]
                self.positions[board_length - 1] = self.prevGuesses[-1][0]

            elif len(self.prevGuesses) > 1 and self.responses[-2][0] - 2 == last_response[0] and self.prevGuesses[-2] != self.prevGuesses[-1]:
                self.positions[0] = self.prevGuesses[-2][0]
                self.positions[board_length - 1] = self.prevGuesses[-2][0]

            elif (len(self.prevGuesses) > 1 and self.responses[-2][0] + 1 == last_response[0] and self.prevGuesses[-2] != self.prevGuesses[-1]):
                for i in range(len(self.prevGuesses[-1])):
                    if self.prevGuesses[-2][i] != self.prevGuesses[-1][i] and i not in self.positions:
                        self.positions[i] = self.prevGuesses[-1][i]

            elif (len(self.prevGuesses) > 1 and self.responses[-2][0] - 1 == last_response[0] and self.prevGuesses[-2] != self.prevGuesses[-1]):
                for i in range(len(self.prevGuesses[-1])):
                    if self.prevGuesses[-2][i] != self.prevGuesses[-1][i] and i not in self.positions:
                        self.positions[i] = self.prevGuesses[-2][i]

            # Fills up missingPositions list and applies positions to the guess
            for i in range(board_length):
                if i not in self.positions.keys():
                    missingPositions.append(i)
                for j in self.positions.values():
                    if i in self.positions.keys() and self.positions[i] == j:
                        guess[i] = j

            # Increments the specific position
            if 0 in missingPositions and guess[0] != colors[-1]:
                guess[0] = colors[colors.index(guess[0]) + 1]
                guess[board_length - 1] = colors[colors.index(guess[board_length - 1]) + 1]
            elif missingPositions and guess[missingPositions[0]] != colors[-1]:
                guess[missingPositions[0]] = colors[colors.index(guess[missingPositions[0]]) + 1]

            self.prevGuesses.append(list_to_str(guess))
            return list_to_str(guess)
