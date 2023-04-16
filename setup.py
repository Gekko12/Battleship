"""
BattleShip Game Setup:
By default 6x6 grid size is used and 3 battleships were constructed
randomly in the grid. Player has to guess the position of the ship
within the grid and destroy them. This setup takes care of logical grid
building.
"""

import sys
from random import randint



class BattleSetup(object):
    """
    Base game setup class. Logical printing of NxN grid with 
    battleships positioned randomly in the grid.
    """

    __MIN_GRIDSIZE = 3
    __MAX_GRIDSIZE = 9
    __SHIP_SIZE = 3 # each ship take 3 cells width


    def __init__(self, gridsize=6, shipcount=3):
        self.gridsize = gridsize
        self.shipcount = shipcount      
        self._max_shipcount = 1 # maximum ship that can be installed in a grid, depends on gridsize
        self._coordinates = list()

    def getgridsize(self):
        return self._gridsize
    

    def setgridsize(self, gridsize):
        try:
            if gridsize < BattleSetup.__MIN_GRIDSIZE or gridsize > BattleSetup.__MAX_GRIDSIZE or gridsize % BattleSetup.__SHIP_SIZE != 0:
                raise ValueError("Grid size should be in the range of [{0}, {1}] and multiple of {2}.".format(BattleSetup.__MIN_GRIDSIZE, BattleSetup.__MAX_GRIDSIZE, BattleSetup.__SHIP_SIZE))
        except ValueError as msg:
            print(msg)
            sys.exit(0)
        else:
            self._gridsize = gridsize
    
    
    gridsize = property(getgridsize, setgridsize)


    def getshipcount(self):
        return self._shipcount
    

    def setshipcount(self, shipcount):
        try:
            # per 3x3 subgrid ie. battleship size, one ship can be installed 
            # except last 3xN subgrid, only one battle ship 
            self._max_shipcount = ((self.gridsize ** 2 - self.gridsize * BattleSetup.__SHIP_SIZE) // BattleSetup.__SHIP_SIZE ** 2) + 1

            if shipcount > self._max_shipcount or shipcount == 0:
                raise ValueError("Battleship count should be in range of [{0}, {1}].".format(1, self._max_shipcount))
        except ValueError as msg:
            print("Error:", msg)
            sys.exit(0)
        else:
            self._shipcount = shipcount
    

    shipcount = property(getshipcount, setshipcount)


    def shipcoordinates(self):
        """
        Generate random non-overlapping ship coordinates,
        horizontally or vertically. Grid is divided into sub grids of
        SHIP_SIZE x SHIP_SIZE. 
        """
        coordinates_count = 0
        for row in range(0, self.gridsize, BattleSetup.__SHIP_SIZE):
            for col in range(0, self.gridsize, BattleSetup.__SHIP_SIZE):
                if coordinates_count >= self.shipcount:
                    return
                # last SHIP_SIZE ie. 3 rows are reserved for 
                # one vertical axis battleship
                if self.gridsize - BattleSetup.__SHIP_SIZE == row:
                    r = row
                    c = randint(0, self.gridsize-1)
                    self._coordinates.append([r, c, "Vertical"])
                    coordinates_count += 1
                else:
                    r = randint(row, row+2)
                    c = col
                    self._coordinates.append([r, c, "Horizontal"])
                coordinates_count += 1


    def gridprint(self):
        """
        Gameplay grid will be printed along with battleships. 
        """
        if not len(self._coordinates):
            self.shipcoordinates()

        self._coordinates.sort() # sort so that row wise printing can happens
        # print("GamePlay Corrdinate:", self._coordinates)

        cord_indx, cord_len = 0, len(self._coordinates)
        row = 0
        vert_char_count = -1

        print("  " + "_" * (2*self.gridsize-1))

        while row < self.gridsize:
            print(chr(65+row), end="") # row-wise alpha denote

            col = 0
            while col < self.gridsize:
                if cord_indx < cord_len:
                    point_r, point_c, axis = self._coordinates[cord_indx]
                if point_r == row and point_c == col and axis == "Horizontal":
                    print("| BT", end="")   #if status == "Not Destroyed" else print("| XX", end="")
                    print(cord_indx+1, end=" ")
                    cord_indx += 1
                    col += 3
                elif point_c == col and (row >= point_r and row <= point_r + 2) and axis == "Vertical":
                    vert_char_count += 1
                    if vert_char_count == 0:
                        print("|B", end="")     #if status == "Not Destroyed" else print("|X", end="")
                    elif vert_char_count == 1:
                        print("|T", end="")     #if status == "Not Destroyed" else print("|X", end="")
                    elif vert_char_count == 2:
                        print("|" + str(cord_indx+1), end="")
                        vert_char_count = -1
                        cord_indx += 1
                    col += 1
                # elif axis == "Vertical":
                #     cord_indx += 1
                #     print("|_", end="")
                #     col += 1
                else:
                    print("|_", end="")
                    col += 1
            print("|")
            row += 1

        # col-wise cell denote as numbers
        print(end=" ")
        for i in range(self.gridsize):
            print(" " + str(i), end="")
        print()


    
if __name__ == "__main__":
    obj = BattleSetup(gridsize=9, shipcount=7)
    obj.shipcoordinates()
    obj.gridprint()
    # print(obj._coordinates)
