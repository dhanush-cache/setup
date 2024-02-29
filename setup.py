from pathlib import Path
import subprocess
import platform
import json


class Setup:
    """Class to setup a coding enviornment."""

    def __init__(self):
        self.pwd = Path().absolute()
        self.home = Path().home()
        self.on_unix = False if platform.system() == "Windows" else True
        self.vsdir = self.osvalue(
            self.home / ".config/Code/User", self.home / r"AppData\Roaming\Code\User"
        )

    def osvalue(self, unix, windows):
        """Return a value based on os."""
        return unix if self.on_unix else windows

    def mkdir(self, *folders):
        """Create folders in the root directory."""
        for folder in folders:
            if not Path(folder).exists():
                Path(folder).mkdir()

    def configure_git(self, level: str = "local", additional: dict = {}):
        """Sets up the git configurations."""
        configs = {
            "user.name": "Anonymous",
            "user.email": "anonymous@example.com",
            "core.editor": "code --wait",
            "core.autocrlf": self.osvalue("input", "true"),
            "init.defaultBranch": "main",
            "credential.helper": "store",
            "diff.tool": "vscode",
            "difftool.vscode.cmd": "code --wait --diff $LOCAL $REMOTE",
            "difftool.prompt": "false",
            "alias.pushit": "bundle create Dhanush.git --all",
        }

        for key, value in additional.items():
            configs[key] = value

        for key, value in configs.items():
            command = ["git", "config", f"--{level}", key, value]
            subprocess.run(command)

    def configure_vscode(self, universal=False, additional: dict = {}):
        """Sets up the vscode settings."""
        self.mkdir("bin", ".vscode")

        bin_file = f"$fileNameWithoutExt.{'out' if self.on_unix else 'exe'}"
        bin_file = str(self.pwd / "bin" / bin_file)

        settings = {
            # Basic settings.
            "window.commandCenter": False,
            "files.autoSave": "off",
            "editor.formatOnSave": True,
            "workbench.editorAssociations": {"git-rebase-todo": "default"},

            # Appearance.
            "workbench.colorTheme": "Dracula",
            "workbench.iconTheme": "material-icon-theme",
            "editor.fontFamily": "JetBrainsMono Nerd Font",
            "terminal.integrated.fontFamily": "UbuntuMono Nerd Font Mono",
            "workbench.panel.defaultLocation": "right",
            "window.zoomLevel": self.osvalue(2.5, 1.2),
            "editor.fontSize": self.osvalue(20, 14),

            # Formatting.
            "[python]": {"editor.defaultFormatter": "ms-python.autopep8"},
            "pylint.args": ["--errors-only"],
            "C_Cpp.clang_format_style": "{BasedOnStyle: Google, IndentWidth: 4}",
            "[shellscript]": {"editor.defaultFormatter": "mkhl.shfmt"},
            "[jsonc]": {"editor.defaultFormatter": "esbenp.prettier-vscode"},

            # code-runner.
            "code-runner.clearPreviousOutput": True,
            "code-runner.ignoreSelection": True,
            "code-runner.saveAllFilesBeforeRun": True,
            "code-runner.showExecutionMessage": False,
            "code-runner.executorMap": {
                "c": f"cd $dir && gcc $fileName -o {bin_file} && {bin_file}",
                "cpp": f"cd $dir && g++ $fileName -o {bin_file} && {bin_file}",
                "python": self.osvalue("python3", "python"),
            },
        }

        for key, value in additional.items():
            settings[key] = value

        settings_json = json.dumps(settings, indent=2)
        settings_file = (
            self.vsdir / "settings.json" if universal else ".vscode/settings.json"
        )
        Path(settings_file).write_text(settings_json)
