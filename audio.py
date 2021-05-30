from kivy.core.audio import SoundLoader

class Sound:
    """
    This is a class that manages the sounds of the game (in the GUI version).
    
    Attributes
    ----------
    on_start: path to the sound played when a new game starts
    on_move: path to the sound played when a tile is played 
    background_sound: path to the background music
    """
    def __init__(self):
        """
        Initializes the class.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.on_start = SoundLoader.load("Sounds/setup.wav")
        self.on_move = SoundLoader.load("Sounds/move.wav")
        self.background_sound = SoundLoader.load("Sounds/f1.wav")
        self.on_start.play()
    
    def onStart(self, state="play"):
        """
        Plays sound on start.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if state=="play":
            self.on_start.play()
    
    def onBackground(self, state="play"):
        """
        Plays background music in a loop if sound is enabled.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if state=="play":
            self.background_sound.play()
            self.background_sound.loop = True
        else:
            self.background_sound.stop()
    
    def onMove(self, state="play"):
        """
        Plays sound on move.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if state=="play":
            self.on_move.play()
    
    def change_sound_state(self):
        """
        Called when the Sound button is pressed.
        It toggles the background music on and off.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.background_sound.state == "play":
            self.onBackground("stop")
        else:
            self.onBackground()