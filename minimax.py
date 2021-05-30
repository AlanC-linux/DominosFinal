from rules import RulesManager
from tile import Tile

class Minimax:
    """
    Class that generates the moves using the Minimax algorithm for the AI player.
    """
    @staticmethod
    def eval_function(game):
        """
        Evaluation function for the game.

        Returns
        -------
        None
        """
        return game.players[0].hand.score() - game.players[1].hand.score()

    @staticmethod
    def minimax(game, current_player, depth):
        """
        Computes of the tree of possible moves at a given depth and finds the best move using the evaluation function.
        
        Parameters
        ----------
        game: the current Game
        current_player: the current player
        depth: the maximum depth of the tree to generate

        Returns
        -------
        A tuple (Tile, side)
        """
        scores = []

        if not RulesManager.has_playable_tile(game.players[current_player].hand, game.board):

            if not RulesManager.has_playable_tile(game.players[(current_player + 1) % 2].hand, game.board):
                null_tile = Tile(-1, -1)
                scores.append((Minimax.eval_function(game), null_tile, ""))
            else:
                scores.append(Minimax.minimax(game, (current_player + 1) % 2, depth))
        else:
            playable_tiles = RulesManager.list_of_playable_tiles(game.players[current_player].hand.tiles, game.board)
            for tile in playable_tiles:

                game.players[current_player].hand.remove(tile[0])
                if depth == 0:
                    scores.append((Minimax.eval_function(game), tile[0], tile[1]))
                else:
                    if tile[1] == 'left':
                        game.board.append_on_left_side(tile[0])
                    else:
                        game.board.append_on_right_side(tile[0])

                    scores.append((Minimax.minimax(game, (current_player + 1) % 2, depth-1)[0], tile[0], tile[1]))

                    if tile[1] == 'left':
                        game.board.remove_leftmost_tile()
                    else:
                        game.board.remove_rightmost_tile()

                game.players[current_player].hand.add_tile(tile[0])

        if game.players[current_player].is_ai:
            scores.sort(reverse  = True, key = lambda i: i[0])
        else:
            scores.sort(key = lambda i: i[0])
        return scores[0]
