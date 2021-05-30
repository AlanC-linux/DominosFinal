from tile import Tile
from board import Board
from player import Player, AI
import xml.etree.ElementTree as ET
from encrypt_decrypt import *
import platform

class XMLUtility:
    """
    This class is used in order to generate a XML representation of a Domino game in order to save and restore games.
    """

    @staticmethod
    def generate_XML_tree_from_game(game):
        """
        Generate a pre-formated XML tree from a Game.

        Parameters
        ----------
        Game: a Domino game.

        Returns
        -------
        tree: a XML tree (xml.etree.ElementTree)
        """

        root = ET.Element("game")

        player1 = ET.Element("player")
        player2 = ET.Element("player")
        board = ET.Element("board")
        undo_stack = ET.Element("undoStack")

        name_player1 = ET.SubElement(player1, "name")
        name_player1.text = game.players[0].name
        name_player2 = ET.SubElement(player2, "name")
        name_player2.text = game.players[1].name

        hand_player1 = ET.SubElement(player1, "hand")
        hand_player1.text = (str(game.players[0].hand))
        hand_player2 = ET.SubElement(player2, "hand")
        hand_player2.text = (str(game.players[1].hand))

        isAI_player1 = ET.SubElement(player1, "isAI")
        isAI_player1.text = str(game.players[0].is_ai)
        isAI_player2 = ET.SubElement(player2, "isAI")
        isAI_player2.text = str(game.players[1].is_ai)

        AImode_player2 = ET.SubElement(player2, "AImode")
        AImode_player2.text = game.players[1].type

        AIdepth_player2 = ET.SubElement(player2, "AIdepth")
        AIdepth_player2.text = str(game.players[1].depth)

        board_first_tile = ET.SubElement(board,"firstTile")
        board_first_tile.text = str(game.board.first_tile)

        board_tiles = ET.SubElement(board, "tiles")
        board_tiles.text = str(game.board)

        undo_stack_tiles = ET.SubElement(undo_stack, "tiles")
        undo_stack_player = ET.SubElement(undo_stack, "player")
        undo_stack_tiles.text = ""
        undo_stack_player.text = ""
        for elem in game.undo_stack:
            undo_stack_tiles.text += str(elem[0])
            undo_stack_player.text += str(elem[1].is_ai) +" "

        root.append(player1)
        root.append(player2)
        root.append(board)
        root.append(undo_stack)

        tree = ET.tostring(root)
        return tree

    @staticmethod
    def write_XML_tree_to_file(tree, file_name):
        """
        Write an XML tree in a text file.

        Parameters
        ----------
        tree: a XML tree
        file_name: a str

        Returns
        -------
        None
        """
        relative_path_to_save_file = file_name
        with open (relative_path_to_save_file, "wb") as fh:
            fh.write(tree)

    @staticmethod
    def get_xml_data(file_name):
        """
        Used to build the Game elements from a XML tree.

        Parameters
        ----------
        file_name: a str (the name of the XML save file)

        Returns
        -------
        A tuple (player, board, undo_stack)
            player is a list of Player objects, with their Hand
            board is a Board
            undo_stack is a stack
        """
        player = []
        board = Board()
        undo_stack_tiles = []
        undo_stack_player = []
        undo_stack = []
        tree = ET.parse(file_name)
        root = tree.getroot()

        for elem in root.findall("./player[isAI = 'False']"):
            player.append(Player())
            player[0].name = elem[0].text
            hand = elem[1].text
            i = 0
            while i < len(hand):
                if hand[i] not in('[', ']', '|', ','):
                    tile = Tile(int(hand[i]), int(hand[i+2]))
                    player[0].hand.add_tile(tile)
                    i += 2
                i += 1

        for elem in root.findall("./player[isAI = 'True']"):
            player.append(AI(elem[3].text, int(elem[4].text)))
            player[1].name = elem[0].text
            hand = elem[1].text
            i = 0
            while i < len(hand):
                if hand[i] not in('[', ']', '|', ','):
                    tile = Tile(int(hand[i]), int(hand[i+2]))
                    player[1].hand.add_tile(tile)
                    i += 2
                i += 1

        for elem in root.findall("./board"):

            i = 0
            board_text = elem[1].text
            if board_text != None:
                while(i < len(board_text)):
                    if board_text[i] not in('[', ']', '|', ','):
                        tile = Tile(int(board_text[i]), int(board_text[i+2]))
                        board.append_on_right_side(tile)
                        i += 2
                    i += 1

                first_tile_text = elem[0].text
                first_tile = Tile(int(first_tile_text[1]), int(first_tile_text[3]))
                board.first_tile = first_tile

        for elem in root.findall("./undoStack"):

            tiles_text = elem[0].text
            player_text = elem[1].text

            i = 0
            if tiles_text != None:
                while i < len(tiles_text):
                    if tiles_text[i] not in ('[', '|', ']'):
                        print(tiles_text[i])
                        tile = Tile(int(tiles_text[i]), int(tiles_text[i+2]))
                        undo_stack_tiles.append(tile)
                        i +=2
                    i +=1

                i = 0
                while i < len(player_text):
                    if player_text[i] == 'F':
                        undo_stack_player.append(player[0])
                    elif player_text[i] == 'T':
                        undo_stack_player.append(player[1])
                    i +=1

            for i in range(len(undo_stack_tiles)):
                undo_stack.append((undo_stack_tiles[i], undo_stack_player[i]))

        return player, board, undo_stack

    @staticmethod
    def save_game_to_xml(current_game, file_name):
        """
        Saves the current game to an XML file.

        Parameters
        ----------
        current_game: the current Game
        file_name: the file name (without extension)
        """
        tree = XMLUtility.generate_XML_tree_from_game(current_game)
        file_path = "saves/" + file_name + ".xml"
        XMLUtility.write_XML_tree_to_file(tree, file_path)
        EncryptDecrypt.encrypt_and_store_file(file_path)

    @staticmethod
    def load_game_from_xml(update, current_game, file_name):
        EncryptDecrypt.decrypt_file(file_name, "xml")
        decrypted_file_name, _ = os.path.splitext(file_name)
        player, board, undo_stack = XMLUtility.get_xml_data(decrypted_file_name + ".xml")
        current_game.players = player
        current_game.board = board
        current_game.undo_stack = undo_stack
        update()
        os.remove(decrypted_file_name+".xml")