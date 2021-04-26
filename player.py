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
    colorsUsed = []         # Holds all correct colors in a given code
    num_bs = 0
    

    
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
#_____________________________________________________ AB Color _______________________________________________________
        if scsa.name == "ABColor":
            if (last_response[2] == 0): #if the first guess of a round
                guess = list_to_str('A'*board_length) #guess all As
                self.num_bs = 0 #reset globals
                self.guesses = []
            if (last_response[2] == 1): #if 2nd guess
                self.num_bs = board_length - last_response[0] #subtract the correct number of positions from the all As guess, since the remaining number of positions will be Bs 
            if (last_response[2] > 0): #if not the first guess
                while True:
                    color = 'A'*board_length #generate an all As guess
                    color = list(color) #turn it into list form to modify
                    possible_indices = random.sample(range(0,board_length), k=self.num_bs) #choose indices to place bs in; the number of indices chosen are equal to the number of B positions that have been determined
                    for i in possible_indices: #change those indices from As to Bs
                        color[i] = 'B'
                    guess = list_to_str(color) #generate the guess
                    if not (guess in self.guesses): #check if the guess has already been made
                        break #if not then make the guess and if so then make a new guess
            self.guesses.append(guess) #save the guess to the list to keep track of the guesses made
            return guess #return the guess
#_____________________________________________________ First Last _______________________________________________________
        if scsa.name == "FirstLast":
            """
            FirstLast scsa strategy is to first identify the color that fills the first and last position, since they're always the
            same. Once that color is found, each following guess will iterate through the other positions until the code is found. The list
            missingPositions keeps track of what positions still need to be found.
            """
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

#_____________________________________________________ UsuallyFewer and PreferFewer _______________________________________________________
        if scsa.name == "UsuallyFewer" or scsa.name == "PreferFewer":
            """
            UsuallyFewer scsa and PreferFewer scsa strategy is to first identify the colors being used. This is done the same way that the TwoColor
            strategy identifies colors and occurance for each color, except there is an extra check for when there are more than 2 colors(if the list
            of correct colors with accurate occurance of each color != the board length, then there is at least one more color to find). After identifying 
            all the colors, player will use list of correct colors and occrances to generate random guesses. With each guess, it'll note any incorrect guesses
            so that it won't attempt that guess again.
            """
            guess = ""
            #print('response: ', last_response)
            #reset variables
            if last_response[2] == 0:       #no previous guesses               
                self.colorsUsed = []        #stores correct colors and occurance of each color

                self.prevGuesses = []
                self.responses = [last_response]
                self.guessnum = 0

            #IDENTIFY COLORS
            if not self.prevGuesses:                     #if this is the first guess
                guess = (colors[0] * board_length)       #first guess is only the first color(ex: AAAA)
                guess = list_to_str(guess)               #convert list to string
                self.prevGuesses.append(guess)           #add guess to record of guesses
                #print('guessnum: ', self.guessnum)
                return(guess)

            if last_response[0] == 0 and last_response[1] == 0 and not self.colorsUsed:         #if a guess was made and nothing was ever found
                if self.guessnum < len(colors) - 1:                                             #if the end of list of colors has not been reached
                    self.guessnum += 1                                                          #+1 guess
                    #print('guessnum: ', self.guessnum)
                guess = (colors[self.guessnum] * board_length)                                  #try the next color
                
            

            if last_response[0] > 0 and len(self.colorsUsed) < board_length:     #if the last guess had a correct color, and not all colors were found yet
                if(self.prevGuesses[-1][-1] not in self.colorsUsed):             #if the color from the previous guess wasn't already recorded
                    for i in range(last_response[0]):                            #for each occurance of color(noted by last_response[0])...
                        self.colorsUsed.append(self.prevGuesses[-1][-1])         #...add color to list of confirmed colors

            if self.colorsUsed and len(self.colorsUsed) != board_length:         #if at least one color was found but not all 
                if self.guessnum < len(colors) - 1:                              #if the end of list of colors has not been reached
                    self.guessnum += 1                                           #+1 guess
                    #print('guessnum: ', self.guessnum)
                guess = (colors[self.guessnum] * board_length)                   #try the next color


            #By now we should know all the colors we need
            #IDENTIFY POSITIONS
            if len(self.colorsUsed) == board_length:                                           #if all colors were found
                guess = list_to_str(random.sample(self.colorsUsed, k = board_length))          #generate a random guess using colors confirmed to be correct
                while guess in self.prevGuesses:                                               #if that guess was already guessed
                    guess = list_to_str(random.sample(self.colorsUsed, k = board_length))      #guess again

            #print('guessnum: ', self.guessnum)
            #print('guess: ', guess)
            #print(self.prevGuesses[-1])
            guess = list_to_str(guess)              #convert guess to string
            self.prevGuesses.append(guess)          #add guess to record of guesses
            return(guess)
        
        # #_____________________________________________________ Mystery 1-5 _______________________________________________________
        if scsa.name[:-1] == "mystery":
            guess = list_to_str(colors[0]*board_length)
            probDist = []
            
            # The prob distributions were made by countin the amount of times each color occured in each position

            if scsa.name[-1] == "1":
                probDist = [
                    {'C': 44, 'E': 50, 'D': 34, 'A': 37, 'B': 35},
                    {'C': 47, 'E': 49, 'D': 41, 'A': 35, 'B': 28},
                    {'C': 48, 'E': 43, 'B': 32, 'D': 32, 'A': 45},
                    {'C': 51, 'E': 47, 'A': 43, 'D': 30, 'B': 29},
                    {'C': 40, 'E': 43, 'A': 41, 'D': 39, 'B': 37},
                    {'C': 53, 'E': 43, 'D': 29, 'A': 45, 'B': 30},
                    {'C': 47, 'E': 44, 'D': 37, 'A': 41, 'B': 31}
                ]

            if scsa.name[-1] == "2":
                probDist =  [
                    {'A': 41, 'D': 48, 'C': 35, 'B': 40, 'E': 36},
                    {'D': 34, 'C': 46, 'E': 44, 'A': 38, 'B': 38},
                    {'C': 36, 'A': 54, 'D': 37, 'B': 41, 'E': 32},
                    {'A': 41, 'D': 48, 'C': 35, 'B': 40, 'E': 36},
                    {'D': 34, 'C': 46, 'E': 44, 'A': 38, 'B': 38},
                    {'C': 36, 'A': 54, 'D': 37, 'B': 41, 'E': 32},
                    {'A': 41, 'D': 48, 'C': 35, 'B': 40, 'E': 36}
                ]

            if scsa.name[-1] == "3":
                probDist = [
                    {'E': 31, 'D': 41, 'C': 44, 'A': 42, 'B': 42},
                    {'A': 40, 'B': 27, 'E': 46, 'D': 49, 'C': 38},
                    {'C': 33, 'B': 43, 'E': 42, 'D': 48, 'A': 34},
                    {'E': 40, 'A': 40, 'B': 48, 'C': 40, 'D': 32},
                    {'E': 40, 'D': 45, 'B': 35, 'C': 34, 'A': 46},
                    {'A': 46, 'C': 40, 'B': 36, 'D': 41, 'E': 37},
                    {'C': 39, 'B': 34, 'A': 48, 'D': 43, 'E': 36}
                ]

            if scsa.name[-1] == "4":
                probDist = [
                    {'B': 28, 'A': 44, 'E': 37, 'C': 49, 'D': 42},
                    {'B': 42, 'A': 38, 'D': 35, 'C': 48, 'E': 37},
                    {'C': 37, 'B': 37, 'D': 46, 'E': 41, 'A': 39},
                    {'A': 36, 'B': 38, 'D': 46, 'E': 45, 'C': 35},
                    {'A': 38, 'D': 40, 'E': 38, 'C': 38, 'B': 46},
                    {'D': 39, 'A': 40, 'B': 50, 'C': 37, 'E': 34},
                    {'D': 42, 'A': 36, 'B': 50, 'E': 31, 'C': 41}
                ]

            if scsa.name[-1] == "5":
                probDist =  [
                    {'C': 27, 'E': 48, 'B': 33, 'A': 43, 'D': 49},
                    {'A': 49, 'D': 28, 'B': 47, 'E': 37, 'C': 39},
                    {'C': 27, 'E': 48, 'B': 33, 'A': 43, 'D': 49},
                    {'A': 49, 'D': 28, 'B': 47, 'E': 37, 'C': 39},
                    {'C': 27, 'E': 48, 'B': 33, 'A': 43, 'D': 49},
                    {'A': 49, 'D': 28, 'B': 47, 'E': 37, 'C': 39},
                    {'C': 27, 'E': 48, 'B': 33, 'A': 43, 'D': 49}
                ]

            for i in range(board_length):
                guess = random.choices(list(probDist[i].keys()), weights=list(probDist[i].values()), k=board_length)
                
            return list_to_str(guess)
