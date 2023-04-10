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
    __MAX_GRIDSIZE = 10
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
            if gridsize < BattleSetup.__MIN_GRIDSIZE or gridsize > BattleSetup.__MAX_GRIDSIZE:
                raise ValueError("Grid size is not in the range of {0} and {1}.".format(BattleSetup.__MIN_GRIDSIZE, BattleSetup.__MAX_GRIDSIZE))
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
            self._max_shipcount = self.gridsize ** 2 // BattleSetup.__SHIP_SIZE ** 2

            if shipcount > self._max_shipcount or shipcount == 0:
                raise ValueError("Battleship count should be in range of {0} and {1}.".format(1, self._max_shipcount))
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
        SHIP_SIZE x SHIP_SIZE. Axis is choosen randomly either Horizontal
        or Vertical to place the ship.
        """
        coordinates_count = 0
        for row in range(0, self.gridsize, BattleSetup.__SHIP_SIZE):
            for col in range(0, self.gridsize, BattleSetup.__SHIP_SIZE):
                if coordinates_count >= self.shipcount:
                    return
                axis = randint(0, 1) # 0 means Horizontal, 1 means Vertical
                if axis == 0:
                    r = randint(row, row+2)
                    c = col
                    self._coordinates.append((r, c, "Horizontal"))
                else:
                    r = row
                    c = randint(col, col+2)
                    self._coordinates.append((r, c, "Vertical"))
                coordinates_count += 1


    def gridprintbefore(self):
        pass

if __name__ == "__main__":
    obj = BattleSetup(6, 4)
    print(obj.gridsize)
    print(obj.shipcount)
    obj.shipcoordinates()
    print(obj._coordinates)