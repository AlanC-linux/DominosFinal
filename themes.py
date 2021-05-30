import os

class Themes:
    """
    This is a class that manages the themes of the game (in the GUI version)

    Attributes
    ----------
    path_to_tame: the path to the folder containing the background images
    themes: list of the names of the files contained in the themes folder
    index_of_current_theme: the index of the current background image starting from the first file in the themes folder
    root: main Kivy window which uses this class
    """
    def __init__(self, root):
        self.path_to_themes = "./Image/themes/"
        self.themes = os.listdir(self.path_to_themes)
        self.index_of_current_theme = 0
        self.root = root

    def change_background(self):
        """
        Called when the user wants to change the background image.
        This is a sequential run through all the images in the theme folder

        Returns
        -------
        None
        """
        self.index_of_current_theme = (self.index_of_current_theme + 1) % len(self.themes)
        self.root.ids.fond.source = os.path.join(self.path_to_themes,self.themes[self.index_of_current_theme])
