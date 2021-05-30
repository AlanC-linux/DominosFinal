import random
from tile import Tile


#from player import Player
class Deck:
    """
    A class to represent a deck of tiles used in a domino game.
    
    ...
    
    Attributes
    ----------
    tiles : list of tile object
        The list of the tiles in the deck
    length : int
        The length of the deck at the beginning of the game
        
    Methods
    -------
    add_tile(tile):
        Add a specified tile in the deck
    add_predefined(max_value):
        Create a complete deck of tiles of a basic domino game
    shuffle():
        Shuffle the deck
    """
    
    def __init__(self):
        """Constructs and initialize the attributes for the Deck object."""
        
        self.tiles = []
        self.length = -1
    
    def add_tile(self, tile):
        """
        Add a specified tile given in the parameters a the end of the deck.
        
        Parameters
        ----------
        tile : tile object
            Contains the value of the tile added
            
        Returns
        -------
        None
        """
        
        self.tiles.append(tile)

    
    def add_predefined(self, max_value):
        """
        Create a complete deck of tiles from 0 to max_value and set the value 
        of length.
        
        Parameters
        ----------
        max_value: int
            The highest value of a tile in the deck
            
        Returns
        -------
        None
        """
        
        for value1 in range(max_value + 1):
            for value2 in range(value1 + 1):
                self.add_tile(Tile(value1, value2))
        self.length = len(self.tiles)
                
    def shuffle(self):
        """Shuffle the deck using the random.shuffle(x) function."""
        
        random.shuffle(self.tiles)
    
    def __str__(self):
        """Redefinition of the behaviour of __str__()."""
        
        return(",".join(str(tile) for tile in self.tiles))

#should be implemented as an unit test
if __name__ == "__main__":

    d = Deck()
    d.add_predefined(6)
    print(d)
    d.shuffle()
    print(d)
