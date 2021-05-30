from player import Player
from player import AI
from cli import CLI
from board import Board
from deck import Deck
from tile import Tile
from rules import RulesManager

class GameManagerForCLI:
    """
    A class used to manage the progress of a complete game in CLI mode.
    The CLI messages are not created and displayed here.

    Attributes
    ----------
    is_over: a bool set to True when the game is finished (a player has no tiles anymore or no other tile can be played)
    current_player: an int set to 0 when the human plays and to 1 when the computer plays.
    number_of_players: an int constant equal to 2 (human vs computer)
    players: list of Player objects
    board: Board object containing the current state of the board
    deck: Deck object: the set of tiles used in the game
    with_draw: a bool constant set to False: play without draw.
    """
    
    def __init__(self):
        """Constructs and initialize the attributes of the Game object."""
        
        self.is_over = False
        self.current_player = -1
        self.number_of_players = -1
        self.players = []
        self.board = Board()
        self.deck = Deck()
        self.with_draw = False
        self.mode = ""
        
    def init_deck(self):
        """
        Initialises the deck by adding tiles and shuffling it.

        Returns
        -------
        None
        """
        self.deck.add_predefined(6)
        self.deck.shuffle()
        
    def init_mode(self):
        """Initialize the game mode"""
        self.mode = CLI.request_mode()
        
    def init_with_draw(self):
        """
        Choose to play with a draw or not.

        Returns
        -------
        None
        """
        
        self.with_draw = CLI.game_with_draw()
        
    def init_ai(self):
        """
        Set the players played by the computer.

        Returns
        -------
        None
        """

        self.players.append(AI())
        self.players[1].name = f"AI_{1}"
        
    def init_players(self):
        """
        Creates the players (human and computer) and creates their hand, fills them with tiles.
        The Computer players are always placed after the human players.
        
        Returns
        -------
        None
        """
        
        if self.mode == "PvE":

            self.players.append(Player())
            self.players[0].name = CLI.request_user_info()
            AI_strength = CLI.request_AI_Strength()
            if AI_strength == 0:
                self.players.append(AI("Random"))
            elif AI_strength == 1:
                self.players.append(AI("Greedy"))
            elif AI_strength  == 2:
                self.players.append(AI("Minimax", 3))
            elif AI_strength  == 3:
                self.players.append(AI("Minimax", 5)) 
            elif AI_strength  == 4:
                self.players.append(AI("Minimax", 8)) 

            self.number_of_players  = 2

        else:

            self.number_of_players = CLI.request_number_of_players()
        
            for i in range(self.number_of_players):
                if i not in range(len(self.players)):
                    self.players.append(Player())
                    self.players[i].name = CLI.request_user_info()
                
        for i in range(len(self.players)): 
            self.players[i].hand.create_from_deck(self.deck, self.number_of_players, self.with_draw)
        
    def player_who_has_tile_in_hand(self,tile):
        """
        Finds if a player has a particular Tile (passed as paramater)
        Parameters
        ----------
        tile: a Tile objects which is equal (==) to the seeked tile
        Returns
        -------
        A Player object (from the players list) if one of the players has the tile passed as parameter in hand, None otherwise.
        """
        for i in range(self.number_of_players):
            if tile in self.players[i].hand:
                return self.players[i]
        return None
    
    def init_board(self):
        """
        Initializes the board.

        Returns
        -------
        None
        """
        if (not(self.with_draw)) and (len(self.deck.tiles) != 0):
            
            self.board.append_on_left_side(self.deck.tiles[0])
    
    def first_player_to_play(self): 
        """
        Determines the first player to play.
        In this version, the Human player always begins.

        Returns
        -------
        None
        """
        max_tile = Tile(6,6)
        self.current_player = self.player_who_has_tile_in_hand((max_tile))      
        while self.current_player == None:
            max_tile.value1 = max_tile.value1 - 1
            max_tile.value2 = max_tile.value2 - 1
            self.current_player = self.player_who_has_tile_in_hand(max_tile)
        
    def init_game(self):
        """
        Initializes the game (deck, players, board, which is first to play)

        Returns
        -------
        None
        """
        self.init_mode()
        self.init_deck()
        if self.mode == 'PvP':
            self.init_with_draw()
        self.init_players()
        self.init_board()
        self.first_player_to_play()
        self.start_game()
        
    def update_game_state(self, tile, side):
        """
        Update the state of the game by placing the played tile on the board and removing it from the player's hand, checking if the game is over.

        Parameters
        ----------
        tile: the Tile object to be played
        side: a string "left" or "right"
        player: a Player object: the player who plays.
        
        Returns
        -------
        None
        """       
        if side == 'left':
            self.board.append_on_left_side(tile)
        else:
            self.board.append_on_right_side(tile)
        self.current_player.hand.remove(tile)
        
        RulesManager.number_of_successive_passes = 0
        
    def game_is_over(self):
        """
        Checks if a game is over.
        
        Returns
        -------
        A bool
        """        
        for p in self.players:
            if len(p.hand) == 0:
                return True
    
        for p in self.players:
            if RulesManager.has_playable_tile(p.hand, self.board):
                return False
            
        return True
    
    def play(self):
        """
        Plays one turn (for human or AI player)

        Returns
        -------
        None
        """
        CLI.prompt_user_to_play(self.current_player)
        CLI.show_board(self.board)
        CLI.show_hand(self.current_player.hand)
        
        if not(RulesManager.has_playable_tile(self.current_player.hand, self.board)):
            if self.current_player.is_ai:
                CLI.nothing_to_play_for_ai()
            else:
                CLI.nothing_to_play()
        else:        
            if self.current_player.is_ai:
                
                temp_hand = self.current_player.hand
                tile_to_play, side = self.current_player.chose_tile_to_play(temp_hand, self)
            
            else:
                tile_to_play = CLI.request_tile_to_play(self.current_player)
                
                while not(RulesManager.is_playable(tile_to_play, self.board)):
                    CLI.error_tile()
                    tile_to_play = CLI.request_tile_to_play(self.current_player)
                
                side = CLI.request_side()
                
                while not(side == 'left' and 
                        RulesManager.is_playable_on_left_side(tile_to_play, self.board) or 
                        side == 'right' and 
                        RulesManager.is_playable_on_right_side(tile_to_play, self.board)):
                    CLI.error_pos()
                    side = CLI.request_side()
                    
            CLI.show_tile_chosen(self.current_player, tile_to_play, side)
            self.update_game_state(tile_to_play, side)
                
    def start_game(self):
        """
        Makes the current game continue between each move. Checks if the game is completed.

        Returns
        -------
        None
        """    
        while not(self.game_is_over()):
            self.play()
            print("\n\n\n")
            self.current_player = self.players[(self.players.index(self.current_player) + 1) % self.number_of_players]  
        
        self.end_game()
            
    def end_game(self):
        """
        Ends a game by computing and displaying the winner.
        Requests if the player wants to start a new game.

        Returns
        -------
        None if the players doesn't want to play a new game.
        A Game object if the player wants to play one more game.
        """
        score_min = 1000
        winner = Player()
        
        for p in self.players:
            
             if p.hand.score() < score_min:
                 score_min = p.hand.score()
                 winner = p
        
        CLI.display_winner(winner)
        
        if (CLI.request_new_game()):
            new_game = GameManagerForCLI()
            return new_game.init_game()
    
if __name__ == "__main__":
    game = GameManagerForCLI()
    game.init_game()

    
