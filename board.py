import collections
from tile import Tile

class Board:
    """
    A class that represents the board of domino game.
    
    ...
    
    Attributes
    ----------
    board : a collection of deque objects
    
    Methods
    -------
    is_empty():
        Determine if the board is empty
    left():
        Returns the value the most on the left side of the board
    right():
        Returns the value the most on the right side of the board
    append_on_left_side():
        Add a tile on the left side of the board
    append_on_right_side():
        Add a tile on the right side of the board
    """
    
    def __init__(self):
        """Constructs and initialize the attribute of a Board object."""
        
        self.board = collections.deque()
        self.first_tile = Tile(-1,-1)
    
    def is_empty(self):
        """
        Determines if the board is empty or not.
        
        Returns
        -------
        A boolean that contains True if the board is empty and False otherwise
        """
        
        return len(self.board) == 0

    def left(self):
        """
        Gets the value the most on the left of the board and returns it.
        
        Returns
        -------
        An int that contains the value of the tile the most on the left 
        according to its orientation.
        """
        if self.is_empty():
            return None
        else:
            left_tile = self.board[0]
            if left_tile.orientation == 0:
                return left_tile.value1
            elif left_tile.orientation == 180:
                return left_tile.value2

    def right(self):
        """
        Gets the value the most on the right of the board and returns it.
        
        Returns
        -------
        An int that contains the value of the tile the most on the right 
        according to its orientation.
        """
        
        if self.is_empty():
            return None
        else:
            right_tile = self.board[-1]
            if right_tile.orientation == 0:
                return right_tile.value2
            elif right_tile.orientation == 180:
                return right_tile.value1

    def append_on_left_side(self, tile):
        """
        Add a tile on the left side of the board. Flips it if necessary.
        
        Parameters
        ----------
        tile : a tile object
            The tile that will be added to the board
            
        Returns
        -------
        None
        """
        if self.is_empty():
            self.first_tile = tile

        elif tile.value2 != self.left():
            tile.flip()

        self.board.appendleft(tile)
    
    def append_on_right_side(self, tile):
        """
        Add a tile on the right side of the board. Flips it if necessary.
        
        Parameters
        ----------
        tile : a tile object
            The tile that will be added to the board
            
        Returns
        -------
        None
        """
        
        if self.is_empty():
            self.first_tile = tile
            
        elif tile.value1 != self.right():
            tile.flip()

        self.board.append(tile)

    def remove_leftmost_tile(self):

        del self.board[0]

    def remove_rightmost_tile(self):

        del self.board[-1]

    def __str__(self):
        """Redefinition of the behaviour of __str__()."""
        
        return ",".join(str(tile) for tile in self.board)

if __name__ == "__main__":
    b = Board()
    t1 = Tile(2,5)
    t2 = Tile(3,5)
    t3 = Tile(0,2)
    t4 = Tile(0,0)
    t5 = Tile(0,6)
    b.append_on_right_side(t1)
    b.append_on_right_side(t2)
    b.append_on_left_side(t3)
    b.append_on_left_side(t4)
    b.append_on_left_side(t5)
    print(b.left(),b.right(),b.board[-1].value1, b.board[-1].value2, b.first_tile, b.board[-1].orientation)
    print(b)
    b.remove_leftmost_tile()
    b.remove_rightmost_tile()
    print(b)