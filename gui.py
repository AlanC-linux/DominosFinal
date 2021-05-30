# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:19:16 2021
"""
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.factory import Factory
from functools import partial
from game_manager_for_gui import GameManagerForGUI
from xml_utility import XMLUtility
from themes import Themes
from audio import Sound
       

class DominoGame(FloatLayout):
    """
    This is the GUI class where the main windows is created and updated.
    """
    
    NUMBER_OF_ROWS = 9
    NUMBER_OF_COLS = 21
         
    def build(self):
        """
        Creates the GUI when the main function is started.

        Returns
        -------
        None
        """

        Window.maximize()

        self.change_board()
        self.theme = Themes(self)

        self.board_repr = [self.NUMBER_OF_COLS * [0] for _ in range(self.NUMBER_OF_ROWS)]       

        self.sound = Sound()

        self.grid_players = []

    def create_main_GUI(self):
        """Calls the popup window that will register the game information."""
        Factory.PopupConfigureGame().open()

    def start_game(self, player_name, level):
        """
        Initialises all the variables used for a game.
        
        Returns
        -------
        None
        """
        self.change_board()
        self.game = GameManagerForGUI(level[0])
        self.game.init_game(player_name)
        self.create_hand_grid()
        self.sound.onBackground()
        self.update_gui_state()


    def when_change_sound_state_button_pressed(self):
        """
        Called when the Sound button is pressed.
        It toggles the sound effects on and off.

        Returns
        -------
        None
        """
        self.sound.change_sound_state()

    def when_save_current_game_button_pressed(self, file_name): 
        """
        Called when the user confirms ths save of the current game.

        Returns
        -------
        None
        """
        XMLUtility.save_game_to_xml(self, self.game, file_name)
            
    def when_load_game_button_pressed(self, file_name):
        """
        Called when the user wants to load a game.

        Returns
        -------
        None
        """
        XMLUtility.load_game_from_xml(self.update_gui_state, self.game, file_name)

    def when_restart_button_pressed(self):
        """
        Called when the user wants to start a new game. The hands are not modified i.e. the tiles are not shuffled once more.

        Returns
        -------
        None
        """
        while len(self.game.board.board) != 0:
            self.game.undo_move()

        self.game.board.first_tile = None
        self.update_gui_state()

    def when_undo_button_pressed(self):
        """
        Called when the user wants to undo the last played move.

        Returns
        -------
        None
        """
        self.game.undo_move()
        self.update_gui_state()
        
    def when_change_background_button_pressed(self):
        """
        Called when the user wants to change the background image.
        This is a sequential run through all the images in the theme folder

        Returns
        -------
        None
        """
        self.theme.change_background()

    
    def when_hint_button_pressed(self):
        """
        Called when the user wants a hint on which tile he should play.

        Returns
        -------
        None
        """
        [tile_to_play, orientation] = self.game.suggest_move_for_human(self.game.players[0].hand)
        self.ids.message_tray.text = f"Play {tile_to_play} on {orientation} side."
        self.ids.message_tray.color = (1, 1, 1, 1)

    def when_restart_button_pressed(self):
        """
        Called when the user want to start a new game.

        Returns
        -------
        None 
        """
        self.remove_widget(self.grid_players[0])
        self.remove_widget(self.grid_players[1])
        Factory.PopupConfigureGame().open()

    def create_hand_grid(self):
        """
        Creates a GridLayout to display a player's Hand.

        Returns
        -------
        None
        """
        for i in range(len(self.game.players)):
            self.grid_players.append(GridLayout(cols = len(self.game.players[i].hand.tiles)))
            self.grid_players[i].size = (50*self.grid_players[i].cols,100)
            self.grid_players[i].size_hint= (None, None)
            if i == 1:
                self.grid_players[i].pos_hint = {'center_x': 0.5, 'top' : 1}

            else:
                self.grid_players[i].pos_hint = {'center_x': 0.5, 'y': 0}

            self.add_tile(self.game.players[i].hand.tiles, i)
            self.add_widget(self.grid_players[i])
            

    def add_tile(self, tiles, index_player):        
        """
        Adds a tile to the GUI rendition of a player's hand.

        Parameters
        ----------
        tiles: a list of Tiles to be added to the player's hand.
        index_player: 0 if it is the human player, 1 otherwise.

        Returns
        -------
        None
        """
        for i, t in enumerate(tiles):
            tile = tiles[i].imageTile(index_player, self.when_tile_selected)
            self.grid_players[index_player].add_widget(tiles[i].widget)

    def when_tile_selected(self, tile, *largs):
        """
        Function called when the user has selected a Tile and clicked on an orientation button (left or right)

        Parameters
        ----------
        tile: the Tile which has been selected (last tile clicked)
        index_player: 0 if it is the human player, 1 otherwise.

        Returns
        -------
        None
        """
        if self.game.check_move_for_human(tile):
            if not(self.ids.message_tray.text == "You can't play this tile on this side"):
                self.ids.message_tray.color = (0,0,0,0)
            self.update_buttons_actions_for_placing_tiles(tile)

        else:
            self.ids.message_tray.text = "Yon can't play this tile"
            self.ids.message_tray.color = (1,1,1,1)

    def update_buttons_actions_for_placing_tiles(self, tile):
        """
        Updates if side selection button action. Called each time a new tile is pressed.

        Parameters
        ----------
        tile: the last pressed tile
        index_player: 0 if it is the human player, 1 otherwise.

        Returns
        -------
        None
        """
        self.ids.left_selection_button.disabled = False
        self.ids.left_selection_button.on_press = partial(self.play_one_turn, "left", tile)
        self.ids.right_selection_button.disabled = False
        self.ids.right_selection_button.on_press = partial(self.play_one_turn, "right", tile)

    def play_one_turn(self, side, tile):
        """
        Plays one turn of the game: manages the tile selected by the human and then displays the computer's move.
        If the computer has no tile to play, the player is warned and it is the end of the turn.
        If the player can't play after the first computer move, the computer continues playing tiles until the human player is able to play again.
        
        Parameters
        ----------
        side: the selected side for the player's move (left or right)
        tile: the selected tile for the player's move

        Returns
        -------
        None
        """
        self.ids.message_tray.color = (0,0,0,0)
        self.ids.left_selection_button.disabled = True
        self.ids.right_selection_button.disabled = True

        if self.game.play_human_turn(tile, side):
            self.ids.message_tray.color = (0,0,0,0)
            self.update_gui_state()

            if self.game.is_over:
                self.display_end_game()
                return 

            tiles_ai_will_play = []

            self.game.play_ai_turn(tiles_ai_will_play)

            if len(tiles_ai_will_play) == 0: 
                self.ids.message_tray.text = "AI has no possible move. Play again"
                self.ids.message_tray.color = (1, 1, 1, 1)

            else:
                self.update_gui_state()
            
            if self.game.is_over:
                self.display_end_game()
                return
        else:
            self.ids.message_tray.text = "You can't play this tile on this side"
            self.ids.message_tray.color = (1,1,1,1)
            self.when_tile_selected(tile)
        
    def update_gui_state(self):
        """
        Updates the GUI state after each move. First computes the new board_repr (internal board representation used for display) and the displays the tiles according to board_repr.
        
        Parameters
        ----------
        side: the side on which the tile is to be played
        tile: the tile to be played
        index_player: 0 if it is the human player, 1 otherwise.

        Returns
        -------
        None
        """

        self.sound.onMove()
        self.board_repr = self.board_to_board_repr()
        self.display_game()

    def display_game(self):
        """
        Updates the display of the player's hands and the board

        Parameters
        ----------
        index_player: 0 if it is the human player, 1 otherwise.

        Returns
        -------
        None
        """
        
        if len(self.game.board.board) > 2:
            self.ids.undo_button.disabled = False
        else:
            self.ids.undo_button.disabled = True

        for i in range(len(self.game.players)):
            self.grid_players[i].clear_widgets()
            self.grid_players[i].cols = len(self.game.players[i].hand.tiles)  
            self.grid_players[i].size = (50*self.grid_players[i].cols,100)
            self.grid_players[i].size_hint = (None, None)
            self.grid_players[i].pos_hint_x = {'center_x': 0.5}
            self.add_tile(self.game.players[i].hand.tiles, i)
        
        self.ids.board.clear_widgets()
    
        for i in range (self.NUMBER_OF_ROWS):
            for j in range(self.NUMBER_OF_COLS):  
                if self.board_repr[i][j] == 0:
                    self.ids.board.add_widget(Image(color = (0,0,0,0)))

                else:
                    self.ids.board.add_widget(Image(source = self.board_repr[i][j]))
        
    def board_to_board_repr(self):
        """
        Computes a board_repr representation from a board object.

        Returns
        -------
        board_repr: the computed board_repr
        """
        if len(self.game.board.board) == 0:
            board_repr = [self.NUMBER_OF_COLS * [0] for _ in range(self.NUMBER_OF_ROWS)]
            return board_repr

        board_repr = [self.NUMBER_OF_COLS*[0] for _ in range(self.NUMBER_OF_ROWS)]
        i, j = self.NUMBER_OF_ROWS // 2, self.NUMBER_OF_COLS // 2 
        board_repr[i][j] = f"Image/tiles/tile{self.game.board.first_tile.value1}_hhr.png"
        board_repr[i][j+1] = f"Image/tiles/tile{self.game.board.first_tile.value2}_bhr.png"
        index = self.game.board.board.index(self.game.board.first_tile) - 1

        if len(self.game.board.board) > 1:

            while index >= 0:
                tile = self.game.board.board[index]
                value1, value2 = self.tile_is_flip(tile)
                i, j, board_repr = self.parcours_left(i, j, (value1, value2), board_repr)
                index -= 1

            i, j = self.NUMBER_OF_ROWS // 2, self.NUMBER_OF_COLS // 2 + 1
            index = self.game.board.board.index(self.game.board.first_tile) +1

            while index < len(self.game.board.board):
                tile = self.game.board.board[index]
                value2, value1 = self.tile_is_flip(tile)
                i, j, board_repr = self.parcours_right(i, j, (value1, value2), board_repr)
                index +=1

        return board_repr

    def add_on_left(self, i, j, tile, board_repr):
        """
        Utility function used to generate board_repr.

        Returns
        -------
        None
        """
        board_repr[i][j-1] = f"Image/tiles/tile{tile[0]}_bhr.png"
        board_repr[i][j-2] = f"Image/tiles/tile{tile[1]}_hhr.png"
        return (i, j-2, board_repr)

    def add_on_top(self, i, j, tile, board_repr):
        """
        Utility function used to generate board_repr.

        Returns
        -------
        None
        """
        board_repr[i-1][j] = f"Image/tiles/tile{tile[0]}_bvr.png"
        board_repr[i-2][j] = f"Image/tiles/tile{tile[1]}_hvr.png"
        return (i-2, j, board_repr)

    def add_on_right(self, i, j, tile, board_repr):
        """
        Utility function used to generate board_repr.

        Returns
        -------
        None
        """
        board_repr[i][j+1] = f"Image/tiles/tile{tile[0]}_hhr.png"
        board_repr[i][j+2] = f"Image/tiles/tile{tile[1]}_bhr.png"
        return (i, j+2, board_repr)

    def add_on_bottom(self, i, j, tile, board_repr):
        """
        Utility function used to generate board_repr.

        Returns
        -------
        None
        """
        board_repr[i+1][j] = f"Image/tiles/tile{tile[0]}_hvr.png"
        board_repr[i+2][j] = f"Image/tiles/tile{tile[1]}_bvr.png"
        return (i+2, j, board_repr)

    def parcours_left(self, i, j, tile, board_repr):
        """
        Utility function used to generate board_repr.

        Returns
        -------
        None
        """
        if j - 2 >= 0 and board_repr[i][j-1] == 0:
            i, j, board_repr = self.add_on_left(i, j, tile, board_repr)
                
        elif i - 2 >= 0 and board_repr[i-1][j] == 0:
            i, j, board_repr = self.add_on_top(i, j, tile, board_repr)

        elif j + 2 < self.NUMBER_OF_COLS and board_repr[i][j+1] == 0:
            i, j, board_repr = self.add_on_right(i, j, tile, board_repr)

        elif i + 2 < self.NUMBER_OF_ROWS and board_repr[i+1][j] == 0:
            i, j, board_repr = self.add_on_bottom(i, j, tile, board_repr)

        return (i, j, board_repr)

    def parcours_right(self, i, j, tile, board_repr):
        """
        Utility function used to generate board_repr.

        Returns
        -------
        None
        """
        if j + 2 < self.NUMBER_OF_COLS  and board_repr[i][j+1] == 0:
            i, j, board_repr = self.add_on_right(i, j, tile, board_repr)

        elif i + 2 < self.NUMBER_OF_ROWS and board_repr[i+1][j] == 0:
            i, j, board_repr = self.add_on_bottom(i, j, tile, board_repr)

        elif j - 2 >= 0 and board_repr[i][j-1] == 0:
            i, j, board_repr = self.add_on_left(i, j, tile, board_repr)

        elif i - 2 >= 0 and board_repr[i-1][j] == 0:
            i, j, board_repr = self.add_on_top(i, j, tile, board_repr)

        return (i, j, board_repr)

    def tile_is_flip(self, tile):
        """
        Utility function used to generate board_repr.

        Returns
        -------
        None
        """
        if tile.orientation == 180:
            return tile.value1, tile.value2

        else:
            return tile.value2, tile.value1

    def display_end_game(self):
        """
        Displays a text announcing the player and the scores

        Returns
        -------
        None
        """
        self.remove_widget(self.grid_players[0])
        self.remove_widget(self.grid_players[1])
        self.change_board()

        list_of_scores = self.game.scores_of_players()

        if list_of_scores[0][1] == list_of_scores[1][1]:
            self.ids.winner.text = "It's a tie !"
        else:
            self.ids.winner.text = f"{list_of_scores[0][0].name} wins !"

        self.ids.scores.text = f"SCORES:\n{list_of_scores[0][0].name} : {list_of_scores[0][1]}\n{list_of_scores[1][0].name} : {list_of_scores[1][1]}"

    def change_board(self):
        """
        Utility function used to create a new game.

        Returns
        -------
        None
        """
        for child in self.children:

            if child.opacity == 0:
                child.disabled = False
                child.opacity = 1
            else:
                child.disabled = True
                child.opacity = 0

        self.ids.fond.opacity = 1
        
        self.ids.message_tray.text = ""
        self.ids.winner.text = "Welcome to Domino Game !"
        
class DominoApp(App):

    def build(self):
        self.domino = DominoGame()
        self.domino.build()
        return self.domino

if __name__ == '__main__':

    DominoApp().run()
