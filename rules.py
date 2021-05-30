from random import choice

class RulesManager:
    """
    A class that creates rules managers for a domino game.
    
    ...
    
    Attributes
    ----------
    None
    
    Methods
    -------
    has_playable_tile(player, board):
        Check if a player can play a tile on a board from his hand
    is_playable_on_left_side(tile, board):
        Check if a tile can be played on the left side of a board 
    is_playable_on_right_side(tile, board):
        Check if a tile can be played on the right side of a board
    """
    @staticmethod
    def has_playable_tile(hand,board):
        """
        Check if a specified player can play a tile on a specified board 
        from his hand.
        
        Parameters
        ----------
        player : Player object
            The player that will have his hand checked tile by tile
        board : Board object
            The board of the current game
            
        Returns
        -------
        A boolean that contains True if the player has a playable tile and 
        False otherwise
        """
        
        if board.is_empty():
            return True
        elif len(hand) == 0:
            return False
        else:
            for element in hand.tiles:
                if (element.value1 == board.left() or 
                    element.value2 == board.left() or 
                    element.value1 == board.right() or 
                    element.value2 == board.right()):
                    return True
            return False

    @staticmethod    
    def is_playable_on_left_side(tile, board):
        """
        Check if a specified tile can be played on the left side of a 
        specified board. 
        
        Parameters
        ----------
        tile : Tile object
            The tile an user chooses to play
        board : Board object
            The board of the current game 
            
        Returns
        -------
        A boolean that contains True if the tile can be played and 
        False otherwise
        """
        
        if board.is_empty():
            return True
        else:        
            if tile.value1 == board.left() or tile.value2 == board.left():
                return True
            else:
                return False

    @staticmethod        
    def is_playable_on_right_side(tile, board):
        """
        Check if a specified tile can be played on the right side of a 
        specified board. 
        
        Parameters
        ----------
        tile : Tile object
            The tile an user chooses to play
        board : Board object
            The board of the current game 
            
        Returns
        -------
        A boolean that contains True if the tile can be played and 
        False otherwise
        """
        
        if board.is_empty():
            return True
        else:
            if tile.value1 == board.right() or tile.value2 == board.right():
                return True
            else:
                return False

    @staticmethod            
    def is_playable(tile, board):
        """
        Check if a specified tile can be played on any side of the board. 
        
        Parameters
        ----------
        tile : Tile object
            The tile an user chooses to play
        board : Board object
            The board of the current game 
            
        Returns
        -------
        A boolean that contains True if the tile can be played and 
        False otherwise
        """        
        if (RulesManager.is_playable_on_left_side(tile, board) or RulesManager.is_playable_on_right_side(tile, board)):
            return True
        else:
            return False
        
    @staticmethod    
    def list_of_playable_tiles(hand, board):
        """
        Generates a list of all playable tiles from a hand, given a particular board.
        
        Parameters
        ----------
        hand : Hand object
            The hand for which to determine playable tiles
        board : Board object
            The board of the current game 
            
        Returns
        -------
        A list of all playable tiles (Tile objects)
        """        
        list_of_tiles = []
        
        for tile in hand:
            if RulesManager.is_playable_on_left_side(tile, board):
                list_of_tiles.append((tile, "left"))
            elif RulesManager.is_playable_on_right_side(tile, board):
                list_of_tiles.append((tile, "right"))
                
        return list_of_tiles
