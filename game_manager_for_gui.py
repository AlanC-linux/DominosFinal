from player import Player
from player import AI
from board import Board
from deck import Deck
from tile import Tile
from rules import RulesManager
import sys

class GameManagerForGUI:
    """
    A class used to manage the progress of a complete game in GUI mode.
    The GUI elements are not created and displayed here.

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
    def __init__(self, AI_strength):
        """
        docstring
        """
        self.is_over = False
        self.current_player = 0 #human
        self.number_of_players = 2         #PvE
        self.players = []
        self.board = Board()
        self.deck = Deck()
        self.with_draw = False
        self.mode = ""
        self.undo_stack = []
        self.hint_AI = AI("Greedy") #used to determine suggested move for human
        self.AI_strength = int(AI_strength)

    def init_deck(self):
        """
        Initialises the deck by adding tiles and shuffling it.

        Returns
        -------
        None
        """
        self.deck.add_predefined(6)
        self.deck.shuffle()
        
    def init_players(self, human_name):
        """
        Creates the 2 players (human and computer) and creates their hand, fills them with tiles.
        
        Returns
        -------
        None
        """
        self.players.append(Player())
        if self.AI_strength == 0:
            self.players.append(AI("Random"))
        elif self.AI_strength == 1:
            self.players.append(AI("Greedy"))
        elif self.AI_strength  == 2:
            self.players.append(AI("Minimax", 3))
        elif self.AI_strength  == 3:
            self.players.append(AI("Minimax", 5)) 
        elif self.AI_strength  == 4:
            self.players.append(AI("Minimax", 8))       
        
        if human_name == ' ':
            self.players[0].name = "Human"
        else:
            self.players[0].name = human_name
        self.players[1].name = "Computer"

        for i in range(self.number_of_players):
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
    
    def first_player_to_play(self): # Probleme si tous les doubles dans la pioche 
        """
        Determines the first player to play.
        In this version, the Human player always begins.

        Returns
        -------
        None
        """
        self.current_player = self.players[0] #human begins
        
    def init_game(self, human_name):
        """
        Initializes the game (deck, players, board, which is first to play)

        Returns
        -------
        None
        """
        self.init_deck()
        self.init_players(human_name)
        self.init_board()
        self.first_player_to_play()

    def check_move_for_human(self, tile_to_play):
        """
        Checks if a move is legal (check done by the RulesManager class)

        Parameters
        ----------
        tile_to_play: a Tile object

        Returs
        ------
        A bool: whether the move is legal
        """
        return RulesManager.is_playable(tile_to_play, self.board)

    def check_move_for_ai(self, tiles_to_play):
        """
        Checks if AI has something to play withing a selection of tiles (check done by the RulesManager class)

        Parameters
        ----------
        tiles_to_play: a list of tiles objects
        
        Returs
        ------
        A bool: whether a move can be played
        """
        return RulesManager.has_playable_tile(tiles_to_play, self.board)

    def suggest_move_for_human(self, hand):
        return self.hint_AI.chose_tile_to_play(hand, self)

    def play_human_turn(self, tile, side):
        """
        Checks if the passed tile can be played on the passed side (using the RulesManager class).
        If this is the case, updates the game state.

        Parameters
        ----------
        tile: a Tile object, tile to play.
        side: a str, the side on which the tile should be played.

        Returns
        -------
        A bool
        """
        if ((side == "left" and RulesManager.is_playable_on_left_side(tile, self.board)) or
             side == "right" and RulesManager.is_playable_on_right_side(tile, self.board)):
            self.update_game_state(tile, side, self.players[0])
            return True
        else:
            return False

    def play_ai_turn(self, tiles_ai_will_play):
        """
        Builds the set of tiles to play by AI and updates the game each time.
        The AI normally plays only once but can play multiple times if the human player has no possible move.
        
        Parameters
        ----------
        tiles_ai_will_play: a list of tiles to be played by AI (can be empty)

        Returns
        -------
        The list of played tiles (after possible recursive calls)
        """
        if  not(self.check_move_for_ai(self.players[1].hand)):
            return tiles_ai_will_play

        else:
            tile = self.players[1].chose_tile_to_play(self.players[1].hand, self)
            tiles_ai_will_play.append(tile)
            self.update_game_state(tile[0], tile[1], self.players[1])

            if RulesManager.has_playable_tile(self.players[0].hand, self.board):
                return tiles_ai_will_play
            #if human can't play, AI plays multiple times
            else:
                return self.play_ai_turn(tiles_ai_will_play)

    
    def update_game_state(self, tile, side, player):
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
        if side == "left":
            self.board.append_on_left_side(tile)

        else:
            self.board.append_on_right_side(tile)

        self.undo_stack.append((tile,player))
        player.hand.tiles.remove(tile)
        self.check_game_over()
                  
        
    def undo_move(self):
        """
        Undoes a complete turn (human and AI moves). The successive moves are stored in a stack.
        Places the tiles back into the players' hands.
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if len(self.undo_stack) == 0:
            return
        
        while self.undo_stack[-1][1].is_ai :

            last_tile_played = self.undo_stack.pop()
            if last_tile_played[0] == self.board.board[0]:
                self.board.remove_leftmost_tile()
            else:
                self.board.remove_rightmost_tile()
            last_tile_played[1].hand.add_tile(last_tile_played[0])
        
        last_tile_played = self.undo_stack.pop()
        if last_tile_played[0] == self.board.board[0]:
            self.board.remove_leftmost_tile()
        else:
            self.board.remove_rightmost_tile()
        last_tile_played[1].hand.add_tile(last_tile_played[0])

    def check_game_over(self):
        """
        Checks if a game is over.
        
        Returns
        -------
        A bool
        """
        #first case: one player has no tiles anymore
        for p in self.players:
            if len(p.hand) == 0:
                self.is_over = True
                return
        #second case: every player can't play (the game is stuck)
        for p in self.players:
            if RulesManager.has_playable_tile(p.hand, self.board):
                self.is_over = False
                return
        self.is_over = True
        return

    def scores_of_players(self):
        """
        Computes the scores of the players and sort the tuples (name, score) by ascending order of score
        
        Returns
        -------
        list_of_scores: the sorted list of tuples (name, score)
        """
        list_of_scores = []
        for p in self.players:
            list_of_scores.append((p, p.hand.score()))

        return sorted(list_of_scores, key = lambda list_of_scores: list_of_scores[1])


    
if __name__ == "__main__":
    game = GameManagerForGUI(0)
    #game.init_game()

    game.players.append(Player())
    game.players.append(AI("Minimax"))
    game.init_deck()
    
    tile3 = Tile(7,7)
    tile4 = Tile(5,3)

    game.players[0].hand.add_tile(tile3)

    game.players[1].hand.create_from_deck(game.deck, 2, False)
    
    game.board.append_on_right_side(tile4)

    tiles = []
    game.play_ai_turn(tiles)
    print(tiles)
    print(game.board)
    