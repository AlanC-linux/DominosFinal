from kivy.uix.button import Button
from kivy.uix.image import Image
from functools import partial
class Tile:
    """
    A class that represents  a tile of a domino game.
    
    ...
    
    Attributes
    ----------
    value1 : int
       The smallest value of the tile 
    value2 : int
        The highest value of the tile
    is_double : bool
        A boolean set to True if the tile is a double and False otherwise
    score : int
        the score of the tile
    orientation : int
        The physcical orientation of a tile once played on the board
        
    Methods
    -------
    rotate():
        Add 90 degrees to the orientation of a tile 
    flip():
        Flip a tile of 180 degrees
    """
        
    def __init__(self, value1, value2):
        """
        Constructs and initialize the attributes of a Tile object 
        with the values given by the parameters.
        
        Parameters
        ----------
        value1 : int
            Save the minimum value between the two given by the parameters
        value2 : int
            Save tha maximum value between the two given by the parameters
            
        Returns
        -------
        None
        """
        
        self.value1 = min(value1, value2)
        self.value2 = max(value1, value2)
        self.is_double = (self.value1 == self.value2)
        self.score = self.value1 + self.value2 + 10*self.is_double
        self.orientation = 0
    
    def rotate(self):
        """
        Make a 90 degrees modulo 360 turn to a tile. This method is used to place 
        a tile on the board.
        
        Returns
        -------
        None
        """
        
        self.orientation = (self.orientation + 90) % 360

    def flip(self):
        """
        Flip a tile by 180 degrees module 360. This method is used to place 
        a tile on the board.

        See rotate() method for more info

        Returns
        -------
        None
        """
        
        self.rotate()
        self.rotate()

    def __eq__(self, other):
        """Redefinition of the behaviour of __eq__()."""
        
        return self.value1 == other.value1 and self.value2 == other.value2
    
    def __str__(self):
        """Redefinition of the behaviour of __str__()."""
        
        if self.orientation == 0:
            return(f"[{self.value1}|{self.value2}]")
        elif self.orientation == 180:
            return(f"[{self.value2}|{self.value1}]")
    
    def __repr__(self):
        """Redefinition of the behaviour of __repr__()."""
        
        return str(self)

    def __contains__(self, value):
        """Redefinition of the behaviour of __contains__()."""
        
        return self.value1 == value or self.value2 == value
    def imageTile(self, index_player, action):
        img_down = "Image/tiles/down.png"
        if index_player == 1:
            src = "Image/tiles/empty.png"
            self.widget = Image(source = src, size = (50,100), size_hint = (None, None))
        else:
            src = f"Image/tiles/tile{self.value1}{self.value2}.png"
            self.widget = Button(background_normal = src, 
                                             background_down = img_down,
                                             size = (50,100), 
                                             size_hint = (None, None), 
                                             on_press = partial(action, self))
        
            

if __name__ == "__main__":
    t = Tile(1,5)
    t.flip()
    print(t)