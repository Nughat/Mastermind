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
    
class Ram2(Player):
    
    def __init__(self):

        self.player_name = "Ram2"
    #globals
    guessnum = 0 #to find 1st color
    guessecondnum = 0 #to find 2nd color based on the 1st color
    guesses = [] #to store all guesses
    
    def make_guess(self, board_length, colors, scsa, last_response):
        
        if (last_response[2] == 0): #at the beginning of a new round reset all globals
            self.guessnum = 0
            self.guessecondnum = 0
            self.guesses = []
        if not self.guesses: #try AAAA on the first guess
            color = colors[self.guessnum] #guessnum has value 0
            guess = list_to_str(color*board_length) #guess will be the 0th element of colors, which is A
        if (self.guesses): #guesses that are not the first guess
            if (last_response[0] == 0 and last_response[1]== 0): #no colors are correct
                self.guessnum = self.guessnum+1 #try the next color in colors
                self.guessecondnum = self.guessnum #update the var for the second color as well, since both colors will be found lexicographically (ex: BBBB has some correct colors, then the second color must be one that comes after B)
                color = colors[self.guessnum] 
                guess = list_to_str(color*board_length)
            elif (last_response[0] == 2): #2 colors in correct position
                color = [colors[self.guessnum],colors[self.guessecondnum+1],colors[self.guessnum],colors[self.guessecondnum+1]] #assume that the colors in the correct position are the 0th and 2nd colors, so change the 1st and 3rd elements 
                guess = list_to_str(color) 
                self.guessecondnum = self.guessecondnum+1 #change the second color alphabetically until it is found   
            elif (last_response[0] == 0 and (last_response[1] == 4 or last_response[1] == 2)): #the assumption from the last condition causes all colors to be in wrong position, meaning that the 1st and 3rd elements were correct and the 0th and 2nd elements need to be changed
                color = self.guesses[-1] #retrieve the previous guess
                color.reverse() #reverse the previous guess
                guess = list_to_str(color)
      
        #print(guess, " ", last_response)
        self.guesses.append(color) #store all guesses in a list in case they are needed later on
        return guess #return the guess