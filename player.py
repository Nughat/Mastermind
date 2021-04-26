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
            """
            TwoColorAlternating scsa strategy is to first determine which two colors are in the code and once these 
            are determined there are two options the answer can be either color1color2color1color2... or 
            color2color1color2color1... so these two guesses are tested
            """
            if last_response[2] == 0:                       #reset all global vars that were used 
                self.prevGuesses = []
                self.colorsUsed = []
                self.guessnum = 0
                self.guessecondnum = 0 
            if not self.prevGuesses:                              #if no prevGuesses guess firstColor * b_l
                guess = (colors[0] * board_length)                #i.e AAAAA
                guess = list_to_str(guess)                        #convert guess to a string
                self.prevGuesses.append(list_to_str(guess))       #add guess to prev guesses
                return guess                                      #return guess
            if (last_response[1] == 0 and last_response[0] == 0): #if no color and pegs match thus guess = nextcol*b_l
                if self.guessnum < len(colors) - 1:               #if guessnum is not exceeding colors highest index
                    self.guessnum = self.guessnum + 1             #increment guessnum
                guess = (colors[self.guessnum]*board_length)      #guess next color x b_l
            if (last_response[0] > 0 and len(self.colorsUsed) < 2):      #if guess had no pegs matched and colorsUsed < 2
                if(self.prevGuesses[-1][-1] not in self.colorsUsed):     #if the color has not already been added
                    #print(self.prevGuesses[-1][-1])
                    self.colorsUsed.append(self.prevGuesses[-1][-1])     #add color to colorsUsed  
                if (self.guessnum < len(colors) - 1 and len(self.colorsUsed) < board_length): #if guessnum > col elements 
                    self.guessnum = self.guessnum + 1                          #and not all cols have been found increment 
                guess = (colors[self.guessnum] * board_length)                 #guessnum and guess next color x b_l
            if (len(self.colorsUsed) == 2):                       #if all colors have been found in code
                guess = ""
                if (self.guessecondnum == 0):                     #guess 1 c1c2c1c2...
                    for i in range(board_length):                 #alternate color1 and color2 board_len times
                        if (i % 2 == 0):                
                            guess = guess + self.colorsUsed[0]
                        if (i % 2 == 1):
                            guess = guess + self.colorsUsed[1]
                if (self.guessecondnum == 1):                     #guess 2 c2c1c2c1...
                    for i in range(board_length):                 #alternate color2 and color1 board_len times
                        if (i % 2 == 0):
                            guess = guess + self.colorsUsed[1]
                        if (i % 2 == 1):
                            guess = guess + self.colorsUsed[0]
                self.guessecondnum = self.guessecondnum + 1       #increment guesscondnum

            guess = list_to_str(guess)                   #convert guess to a string
            self.prevGuesses.append(list_to_str(guess))  #add guess to previous guesses
            #print("colorUsed:", self.colorsUsed)
            #print("prevGuesses:", self.prevGuesses)
            #print("guess: ",guess)
            return guess 
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
        
#_______________________________________________ Two Color ___________________________________________________ 
        if scsa.name == "TwoColor":
            """
            TwoColor scsa strategy is to first determine which two colors are in the code. If the colors are
            A to G it will first guess each color x board_length until it finds the two colors used in the code.
            When it finds that a color is in the code it also notes how many times that color appears in the code
            to reduce the plausible pool of guesses. After all (board_length) elements of the code are added to 
            a list these elements are combined in different random ways that were not previously guessed until
            the correct code has been guessed.
            """
            guess = ""
            if last_response[2] == 0:                       #reset all global vars that were used 
                self.prevGuesses = []
                self.colorsUsed = []
                self.guessnum = 0
            if not self.prevGuesses:                              #if no prevGuesses guess firstColor * b_l
                guess = (colors[0] * board_length)                #i.e AAAAA
                guess = list_to_str(guess)                        #convert guess to a string
                self.prevGuesses.append(list_to_str(guess))       #add guess to prev guesses
                return guess                                      #return guess
            if (last_response[1] == 0 and last_response[0] == 0): #if no color and pegs match thus guess = nextcol*b_l
                if self.guessnum < len(colors) - 1:               #if guessnum is not exceeding colors highest index
                    self.guessnum = self.guessnum + 1             #increment guessnum
                guess = (colors[self.guessnum]*board_length)      #guess next color x b_l
            if (last_response[0] > 0 and len(self.colorsUsed) < board_length): #if last guess has one of the pegs colors
                if(self.prevGuesses[-1][-1] not in self.colorsUsed):           #if the color has not already been added
                    #print(self.prevGuesses[-1][-1])
                    for i in range(last_response[0]):                          #add color into colors used amount of 
                        self.colorsUsed.append(self.prevGuesses[-1][-1])       #times it appeared in last guess
                if (self.guessnum < len(colors) - 1 and len(self.colorsUsed) < board_length): #if guessnum > col elements 
                    self.guessnum = self.guessnum + 1                          #and not all cols have been found increment 
                guess = (colors[self.guessnum] * board_length)                 #guessnum and guess next color x b_l
            if (len(self.colorsUsed) == board_length):                         #if all col and frequency of cols have been found
                guess = list_to_str(random.sample(self.colorsUsed, k = board_length))       #guess random combo w found colors
                while (guess in self.prevGuesses):                                          #make sure guess hasnt already been 
                    guess = list_to_str(random.sample(self.colorsUsed, k = board_length))   #guessed if so make another one until
                                                                                            #you have a new guess
            guess = list_to_str(guess)                   #convert guess to a string
            self.prevGuesses.append(list_to_str(guess))  #add guess to previous guesses
            #print("colorUsed:", self.colorsUsed)
            #print("prevGuesses:", self.prevGuesses)
            #print("guess: ",guess)
            return guess                                 #return guess

#_______________________________________________ Only Once ___________________________________________________ 
        if scsa.name == "OnlyOnce":
            """
            OnlyOnce scsa strategy is to determine which of the colors in colors are in the code. Once these colors
            are dicerned they are added to a list. Once all pegs colors are determined, random guesses with these 
            peg colors are made until the correct guess is generated.
            """
            guess = ""
            if last_response[2] == 0:                       #reset all global vars that were used 
                self.prevGuesses = []
                self.colorsUsed = []
                self.guessnum = 0
            if (len(colors) == board_length): 
                guess = list_to_str(random.sample(colors, k = board_length))       #guess random combo w colors
                while (guess in self.prevGuesses):                                          #make sure guess hasnt already been 
                    guess = list_to_str(random.sample(colors, k = board_length))   #guessed if so make another one until
                guess = list_to_str(guess)                   #convert guess to a string
                self.prevGuesses.append(list_to_str(guess))  #add guess to prev guesses
                return guess   
                
            if not self.prevGuesses:                        #if no prevGuesses guess firstColor*b_l
                guess = (colors[0] * board_length)
                guess = list_to_str(guess)                  #convert guess to a string
                self.prevGuesses.append(list_to_str(guess)) #add guess to prev guesses
                return guess                                #return guess
            
            if (last_response[1] == 0 and last_response[0] == 0): #if no color and pegs match thus guess = nextcol*b_l
                if self.guessnum < len(colors) - 1:               #if guessnum is not exceeding colors index
                    self.guessnum = self.guessnum + 1             #increment guessnum
                guess = (colors[self.guessnum]*board_length)      #guess next color x b_l
            if (last_response[1] == 0 and last_response[0] == 1 and len(self.colorsUsed) < board_length): 
                #if prevoius guess has one of the pegs colors
                if(self.prevGuesses[-1][-1] not in self.colorsUsed):    #if the color has not already been added
                    self.colorsUsed.append(self.prevGuesses[-1][-1])    #add color to the usedColors list
                if self.guessnum < len(colors)-1:                       #if guessnum is not exceeding colors index
                    self.guessnum = self.guessnum + 1                   #increment guessnum
                guess = (colors[self.guessnum] * board_length)          #guess next color x b_l
            if (len(self.colorsUsed) == board_length and last_response[1] <= board_length): #if all b_l cols were found
                guess = list_to_str(random.sample(self.colorsUsed, k = board_length))       #guess random combo w found colors
                while (guess in self.prevGuesses):                                          #make sure guess hasnt already been 
                    guess = list_to_str(random.sample(self.colorsUsed, k = board_length))   #guessed if so make another one until
                                                                                            #you have a new guess
            guess = list_to_str(guess)                   #convert guess to a string
            self.prevGuesses.append(list_to_str(guess))  #add guess to prev guesses
            #print("colorUsed:", self.colorsUsed)
            #print("prevGuesses:", self.prevGuesses)
            #print("guess: ",guess)
            return guess                                 #return guess
