from pathlib import Path
import subprocess
import platform


class Setup:
    """Class to setup a coding enviornment."""

    def __init__(self):
        self.pwd = Path().absolute()
        self.on_unix = False if platform.system() == "Windows" else True

    def osvalue(self, unix, windows):
        """Return a value based on os."""
        return unix if self.on_unix else windows

    def mkdir(self, *folders):
        """Create folders in the root directory."""
        for folder in folders:
            if not Path(folder).exists():
                Path(folder).mkdir()
