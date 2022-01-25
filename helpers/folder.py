import os
from pathlib import Path

class Folder(object):
    def __init__(self):
        self.temp = str(Path().absolute())+os.path.sep+'temp'
    def temp_subfolder(self, folder):
        return self.temp+os.path.sep+folder
