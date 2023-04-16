"""
BattleShip GamePlay:
Player will have unlimited chances to guess the battleship position. Once a 
player guessed a correct cell, that cell will be removed from the play. Once 
all the cells associated with a battleship is removed from the play, the Game has to 
print "Battleship x has sunk". Player can quit after one or more successful sinking 
of ships, and the game has to print a score before quitting.
"""

from setup import BattleSetup



class BattleGamePlay(object):
    """
    Logical elimination of battleship cells which were destroyed.
    And printing of player score at the end of game.
    """

    def __init__(self):
        self.setup = BattleSetup()   # setup building
        self.player = None
        self.player_score = 0
        self.ship_hit_cells = dict() # store ship hit cells with respect to ships
        self.hit_cell_lst = list() # store ship hit cells 

    def playername(self):
        """
        Get the player name from user.
        """
        self.player = input("Enter your name: \n")
    

    def gameinstruction(self):
        """
        Instructions of game will be display.
        """
        print(" Game Manual ".center(80, "*"))

        print("Sample Grid:")
        print("  " + "_" * (2*self.setup.gridsize-1))

        for row in range(self.setup.gridsize):
            print(chr(65+row), end="") # row-wise alpha denote
            col = 0
            while col < self.setup.gridsize:
                if row == 1 and col == 0:
                    print("| BT1 ", end="")
                    col += 3
                else:
                    print("|_", end="")
                    col += 1
            print("|")

        # col-wise cell denote as numbers    
        print(end=" ")
        for i in range(self.setup.gridsize):
            print(" " + str(i), end="")
        print("\n")

        print("A. BT1 is the battleship which located in the cell B0, B1 and B2.")
        print("B. You have to guess the battleship cells to destroy it.")
        print("C. Invalid cells will not count for scoring.")
        print("D. Enter 'Q' to quit the game.")
        print("*" * (80))


    def iscellavailable(self, cell):
        """
        Checks wheather cell is avilable or not for the following grid. 
        """ 
        available_cells = list()
        for c in range(self.setup.gridsize):
            for r in range(self.setup.gridsize):
                available_cells.append(chr(65+c) + str(r))
        # print(available_cells)
        return cell in available_cells


    def isshiphit(self, cell):
        """
        Checks wheather ship is hit or not.
        Returning 0 as False and if shit hit then ship number as True
        """
        if cell in self.hit_cell_lst:
            return 0  # ship already hit

        cell_row, cell_col = ord(cell[0])-65 , int(cell[1])

        for idx, coordinates in enumerate(self.setup._coordinates):
            cord_row, cord_col, axis = coordinates

            if axis == "Horizontal":
                if cord_row == cell_row and (cord_col <= cell_col and (cord_col + 2) >= cell_col):
                    if cell not in self.hit_cell_lst:
                        self.hit_cell_lst.append(cell)  
                        self.ship_hit_cells[idx+1].append(cell) # update ship cell ie. destroyed
                    return  idx + 1 # hit happens
            elif axis == "Vertical":
                if cord_col == cell_col and (cord_row <= cell_row and ((cord_row + 2) >= cell_row)):
                    if cell not in self.hit_cell_lst:
                        self.hit_cell_lst.append(cell)
                        self.ship_hit_cells[idx+1].append(cell)
                    return idx + 1
        return 0
    

    def play(self):
        """
        Game play happens here, with unlimited chances given to 
        player to guess cell.
        """
        if not self.player:
            self.playername()
        
        # build the ships
        self.setup.shipcoordinates()
        # self.setup.gridprint()

        for ship in range(self.setup.shipcount):
            self.ship_hit_cells[ship + 1] = list()

        no_of_guess = 0
        no_of_hit = 0

        while True:
            cell = str(input("Guess a Cell: ")).strip().upper()

            if cell == "Q":
                break
            elif not self.iscellavailable(cell):
                print("Invalid cell !")
            else:
                ship_num = self.isshiphit(cell)
                if not ship_num:
                    print("Miss")
                else:
                    print("Hit")
                    no_of_hit += 1
                    if len(self.ship_hit_cells[ship_num]) == self.setup._BattleSetup__SHIP_SIZE:   # Battlesip sinks logic
                        print("Battelship {0} ie. BT{1} sinks.".format(ship_num, ship_num))
                no_of_guess += 1
        
        try:
            self.player_score = (no_of_hit / no_of_guess) * 100
        except ZeroDivisionError:
            print("-" * 30) 
            print("Player Score:", 0) # when user doesn't take any chance
        else:
            print("-" * 30)
            print("Player Score: {0:.2f}".format(self.player_score))
        print("-" * 30)

        # displaying actual grid
        print("Actual Grid with Battleships.")
        self.setup.gridprint()


# ######################################################################### #
if __name__ == "__main__":
    obj = BattleGamePlay()
    obj.gameinstruction()
    obj.playername()
    obj.play()
