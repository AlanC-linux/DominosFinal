from hand import Hand
from rules import RulesManager
from random import choice
from minimax import Minimax

class Player:
    """
    A class that represents a player in a domino game.
    
    ...
    
    Attributes
    ----------
    name : str
        The name of the player
    position : int
        The geographical position of the player around the table
    hand : Hand object
        The hand of the player
    is_ai: bool
        True is the player is an AI, false otherwise
        
    Methods
    -------
    
    wants_to_play():
        The player chooses a tile from his hand that he wants to play
    side_to_play():
        The player chooses the side of the board on wich he wants to play
    """
    
    def __init__(self):
        """Constructs and initialize the attributes of the Player object."""
        
        self.name = ""
        self.position = -1
        self.hand = Hand() 
        self.is_ai = False
        
class AI(Player):
    """
    A class that represents a computer player in a domino game. It inherits from Player.

    Attributes
    ----------
    name : str
        The name of the player
    position : int
        The geographical position of the player around the table
    hand : Hand object
        The hand of the player
    is_ai: bool
        True is the player is an AI, false otherwise
    type: str
        The AI type (random, greedy, Minimax)
    depth: int
        The depth used to compute the moves for the Minimax algorithm (defaults to 1 for Random and Greedy AI).
    """
    def __init__(self, ai_type, depth = 1):
        
        Player.__init__(self)
        self.is_ai = True
        self.type = ai_type
        self.depth = depth
    
    def chose_tile_to_play(self, hand, game):
        """
        Choses the tile to play for the computer player, given a Board and a Hand.

        Parameters
        ----------
        hand: the computer's hand
        board: the current Board
        game: 

        Returns
        -------
        """

        if self.type == "Random":
            playable_tiles = RulesManager.list_of_playable_tiles(hand.tiles, game.board)
            return choice(playable_tiles)

        elif self.type == "Greedy":
            #Greedy approach: plays the tile with the highest score
            playable_tiles = RulesManager.list_of_playable_tiles(hand.tiles, game.board)
            playable_tiles.sort(key = lambda tile: tile[0].score, reverse=True)
            return playable_tiles[0]

        elif self.type == "Minimax": 

            if min(len(game.players[0].hand), len(game.players[1].hand)) < self.depth:
                self.depth = min(len(game.players[0].hand), len(game.players[1].hand))
            
            t = Minimax.minimax(game, 1, self.depth)
            return (t[1], t[2])
        
if __name__ == '__main__':
    
    test = AI("Minimax")
    test.name = "moi"
    print(test.name, test.is_ai)
         
         
        
        

        