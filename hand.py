from deck import Deck

class Hand:
    """
    A class that represent the hand of tiles that belongs to a player 
    in a domino game.
    
    ...
    
    Attributes
    ----------
    tiles = list of tile object
        List of the tiles within the hand
    
    Methods
    -------
    add_tile(tile):
        Add a specified tile in the hand of its owner
    score():
        Calculate the score of the hand
    play(tile):
        Remove a tile from the hand in order to play it on the board
    create_from_deck_without_draw(deck, number_of_player):
        Create the hand of the player in a game without draw
    create_from_deck_with_draw(deck, number_of_player):
        Create the hand of the player in a game with draw
    """
    
    def __init__(self):
        """Constructs and initialize the attribute for the Hand object."""
        
        self.tiles = []
    
    def add_tile(self, tile):
        """
        Add a specified tile given in the parameters at the end of the hand.
        
        Parameters
        ----------
        tile : tile object
            Contains the value of the tile added
            
        Returns 
        -------
        None
        """
        tile.orientation = 0
        self.tiles.append(tile)

    def score(self):
        """Returns the sum of the values of the tiles in the hand."""
        
        return sum(tile.score for tile in self.tiles)
    
    def remove(self, tile):
        """Search for a tile in the hand, remove and returns it.""" 
        
        index_in_hand = self.tiles.index(tile)
        return self.tiles.pop(index_in_hand)
    
    def create_from_deck(self, deck, number_of_players, with_draw):
        """
        Create the hand of a player in a game without draw according to 
        the number of players present in the game.
        
        Parameters
        ----------
        deck : deck object
            The hand of the player is creating from the deck
        number_of_players : int
            The number of players involved in the game, it's used to know 
            how many tiles each player will have
            
        Returns
        -------
        None
        """
            
        if with_draw == True:
        
            if number_of_players > 2:
                
                for element in deck.tiles[0:6] :
                    self.add_tile(element)
                del deck.tiles[0:6]
            else:
                for element in deck.tiles[0:7]:
                   self.add_tile(element)
                del deck.tiles[0:7]
        else:

            for element in deck.tiles[0:deck.length // number_of_players]:
                self.add_tile(element)
            del deck.tiles[0:deck.length // number_of_players]
                
    def __contains__(self, other_tile):
        """Redefinition of the behaviour of the 'in' method."""
    
        for tile_in_hand in self.tiles:
            if (tile_in_hand.value1 == other_tile.value1 
            and tile_in_hand.value2 == other_tile.value2):
                return True
        return False

    def __len__(self):
        """Redefinition of the behaviour of 'len()'."""
        
        return len(self.tiles)

    def __str__(self):
        """Redefinition of the behaviour of 'print()'."""
        
        return ','.join(str(tile) for tile in self.tiles)

    def __repr__(self):
        """Defines the string representation of the object."""
        
        return str(self)
    
if __name__ == "__main__":
    d = Deck()
    d.add_predefined(6)
    print(d)
    d.shuffle()
    print(d)
    h = Hand()
    h2 = Hand()
    h3 = Hand()
    h.create_from_deck(d,3, False)
    print(h)
    print(d)
    h2.create_from_deck(d,3, False)
    print(h2)
    print(d)
    h3.create_from_deck(d,3, False)


    print(h3)
    print(d)