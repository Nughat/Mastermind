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

    guessnum = 0
    guessecondnum = 0
    guesses = []
    
    def make_guess(self, board_length, colors, scsa, last_response):
        
        if (last_response[2] == 0):
            self.guessnum = 0
            self.guessecondnum = 0
            self.guesses = []
        if not self.guesses:
            color = colors[self.guessnum]
            guess = list_to_str(color*board_length)
        if (self.guesses):
            if (last_response[0] == 0 and last_response[1]== 0):
                self.guessnum = self.guessnum+1
                self.guessecondnum = self.guessnum #B = 1
                color = colors[self.guessnum]
                guess = list_to_str(color*board_length)
            elif (last_response[0] == 2): #2 colors in correct position
                color = [colors[self.guessnum],colors[self.guessecondnum+1],colors[self.guessnum],colors[self.guessecondnum+1]]
                guess = list_to_str(color)
                self.guessecondnum = self.guessecondnum+1    
            elif (last_response[0] == 0 and (last_response[1] == 4 or last_response[1] == 2)):
                color = self.guesses[-1]
                color.reverse()
                guess = list_to_str(color)
      
        #print(guess, " ", last_response)
        self.guesses.append(color)
        return guess