class CLI():
    """
    A class that handles the displays on the screen 
    and the interactions with the users
    when using the Command Line Interface
    
    ...
    
    Attributes
    ----------
    None
    
    Methods
    -------
    error():
        Displays an error message when the user enters an invalid answer
    error_tile():
        Displays an error message when the user picked a wrong tile to play
    error_pos():
        Displays an error message when the user picked a wrong side to play
    request_number_of_ai()
        Requests the number of AI players (automatically played by the computer)
    request_user_info():
        Asks and returns the user's name
    prompt_user_to_play(player):
        Displays the name of the next user to play
    request_number_of_players():
        Asks and returns the number of players about to play
    game_with_draw():
        Asks and returns if the next game will be with or without a draw
    request_mode()
        Allows the user to chose to play in PvP mode (only humans) or PvE mode (human(s) vs engine(s))
    show_hand(hand):
        Displays the specified hand
    show_board(board):
        displays the specified board
    show_tile_chosen()
        Shows the tile played by a player (human or engine) to the user.
    request_tile_to_play():
        Asks and returns the tile the user wants to play
    request_side():
        Asks and returns the side the user choose to play on
    nothing_to_play()
        Displays a message when a player has no tile to play.
    nothing_to_play_for_ai()
        Displays an information to the user when the computer has nothing to play.
    diplay_winner()
        Displays the passed player as the winner of the game.
    request_new_game()
        Asks the user if he/she wants to start a new game.
    request_AI_Strength()
        Asks the user to choose the strength of the AI (between 0 and 4).
    """
    
    def error():
        """
        Displays an error message if the user entered an invalid answer.
        
        Returns
        -------
        None
        """
        
        print("ERROR: You entered an invalid answer, please try again.\n")
        
    def error_tile():
        """
        Displays an error message when the user picked a tile he can't play.
        
        Returns
        -------
        None
        """
        
        print("ERROR: You can't play this tile, choose another one\n")
        
    def error_pos():
        """
        Displays an error message when the user picked a wrong side to play.
        
        Returns
        -------
        None
        """
        
        print("ERROR: You can't put this tile on this side.\n")
        
    def request_number_of_ai():
        """
        Requests the number of AI players (automatically played by the computer)

        Returns
        -------
        An int which is the desired number of AI players.
        """
        
        number_of_ai = input("Please choose how many ai there wille be in this game:\n--> 1\n--> 2\n--> 3\n")
        
        while number_of_ai not in ('1', '2', '3'):
            CLI.error()
            return CLI.request_number_of_ai()
            
        return int(number_of_ai)
        
    def request_user_info():
        """
        Asks and returns the user's name.
        
        Returns
        -------
        name : str
            Contains the name the user entered
        """
        
        name = input(("Please, enter your name:\n"))
        return name
    
    def prompt_user_to_play(player):
        """
        Displays the name of the next user to play.
        
        Parameters
        ----------
        player : Player object
            Uses to display the player's name
            
        Returns
        -------
        None
        """
        
        print(player.name,", it's your turn to play\n")
        
    def request_number_of_players():
        """
        Asks and returns the number of players involved in the game.
        
        Returns
        -------
        An int that contains the input of the user
        """
        
        number_of_players = input("Please, choose how many human player there will be in "
                         "this game:\n--> 1\n--> 2\n--> 3\n--> 4\n")
        
        while number_of_players not in ('1', '2', '3', '4'):
            CLI.error()
            return CLI.request_number_of_players()
            
        return int(number_of_players)

    def game_with_draw():
        """
        Asks to the user and returns if the next game will be 
        with or without a draw.
        
        Returns
        -------
        draw : str
            Contains the input of the user
        """
        draw = input("Please, choose if you to play with or without a draw:\n"
                     "With --> 1\nWithout --> 2\n")
        if draw == '1':
            return True
        
        elif draw == '2':    
            return False
        
        else: 
            CLI.error()
            return CLI.game_with_draw()
        
    def request_mode():
        """
        Allows the user to chose to play in PvP mode (only humans) or PvE mode (human(s) vs engine(s))
        
        Returns
        -------
        A string: 'PvP' or 'PvE' according to the user's choice.
        """
        mode = input("Please choose how you want to play:\nMode PvE ---> 1\nMode PvP ---> 2\n")
        
        if mode == '1':
            return "PvE"
        
        elif mode == '2':
            return "PvP"
        
        else:
            CLI.error()
            return CLI.request_mode()
        
    def show_hand(hand):
        """
        Displays the specified hand.
        
        Parameters
        ----------
        hand : Hand object
            The hand that needs to be displayed
            
        Returns
        -------
        None
        """
        
        print(hand,"\n")
        
    def show_board(board):
        """
        Displays the specified board.
        
        Parameters
        ----------
        board : Board object
            The board that needs to be displayed
            
        Returns
        -------
        None
        """
        
        print(board,"\n")
    
    def show_tile_chosen(player, tile, side):
        """
        Shows the tile played by a player (human or engine) to the user.

        Returns
        -------
        None
        """

        if player.is_ai :
            print(f"Computer choses to play {tile} on {side} side.\n")
            
        else:
            print(f"{player.name} choses to play {tile} on {side} side.\n")

    def request_tile_to_play(player):
        """
        Asks and returns the tile the user wants to play
        
        Returns
        -------
        index : int
            Contains th index of the tile in the hand of the player
        """

        index = int(input("Choose what tile you want to play and enter its "
                          "position, starting the count to 1:\n"))
        
        while index not in range(1,len(player.hand.tiles)+1):   
            CLI.error()
            return CLI.request_tile_to_play(player)
            
        return player.hand.tiles[index-1]
    
    def request_side():
        """
        Asks and returns the side the user choose to play on

        Returns
        -------
        side : str
            Contains the side chossed by the user
        """
        
        side = input("What side do you want to play your tile ?"
                     "\nLeft --> 1\nRight --> 2\n")
        
        if side == '1':
            return 'left'
        
        elif side == '2':
            return 'right'
        
        else:
            CLI.error()
            return CLI.request_side()
    
    def nothing_to_play():
        """
        Displays a message when a player has no tile to play.

        Returns
        -------
        None.
        """
        
        print("You don't have a playable tile.\n")

    def nothing_to_play_for_ai():
        """
        Displays an information to the user when the computer has nothing to play.

        Returns
        -------
        None
        """

        print("The computer player does not have any playable tile. It's the end of its turn.\n")

    def display_winner(player):
        """
        Displays the passed player as the winner of the game. Does not computes which player is the winner.

        Parameters
        ----------
        player: Player object

        Returns
        -------
        None
        """
        print(f"The game is over !\nCongratulations {player.name}, you won with a score of {player.hand.score()} !\n")

    def request_new_game():
        """
        Asks the user if he/she wants to start a new game.
        Returns
        -------
        A bool
        """
        new_game = input("Do you want to play another time ?\nYes --> 1\nNo --> 2\n")
        
        if new_game == '1':
            return True
        
        elif new_game == '2':
            return False
        
        else:
            CLI.error()
            return CLI.request_new_game()
                   
    def request_AI_Strength():
        """
        Ask the user the AI's difficulty.

        Returns
        -------
        an int : The AI's strength
        """
        AI_strength = int(input("Choose tha AI's difficulty:\n0 --> Novice\n1 --> Beginner\n2 --> Intermediate\n3 --> Hard\n4 --> Expert\n"))

        if AI_strength in (1,2,3,4):
            return AI_strength
        
        else:
            CLI.error()
            return CLI.request_AI_Strength()
