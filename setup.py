from pathlib import Path
import subprocess
import platform


class Setup:
    """Class to setup a coding enviornment."""

    def __init__(self):
        self.pwd = Path().absolute()
        self.on_unix = False if platform.system() == "Windows" else True
