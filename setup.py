import os
from pathlib import Path
import subprocess
import platform
import json
import shutil


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
            Path(folder).mkdir(parents=True, exist_ok=True)

    def add_gitignore(self, lang: str):
        """Writes data to the .gitignore file."""
        import requests

        url = f"""https://raw.githubusercontent.com/github/gitignore/main/{
            lang}.gitignore"""
        response = requests.get(url)

        gitignore = response.text
        gitignore += """
# personal
.vscode
"""

        Path(".gitignore").write_text(gitignore)

    def configure_git(self, level: str = "local", lang: str = "", additional: dict = {}):
        """Sets up the git configurations."""
        if level == "local":
            shutil.rmtree(".git", ignore_errors=True)
            subprocess.run(["git", "init", "--initial-branch=main"])
            if lang:
                self.add_gitignore(lang)

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

        configs.update(additional)

        for key, value in configs.items():
            command = ["git", "config", f"--{level}", key, value]
            subprocess.run(command)

    def configure_vscode(self, universal=False, additional: dict = {}):
        """Sets up the vscode settings."""
        self.mkdir(".vscode")

        settings = {
            # Basic settings.
            "window.commandCenter": False,
            "files.autoSave": "off",
            "editor.formatOnSave": True,
            "workbench.editorAssociations": {"git-rebase-todo": "default"},

            # Appearance.
            "workbench.colorTheme": "Dracula",
            "workbench.iconTheme": "material-icon-theme",
            "editor.fontFamily": "JetBrains Mono",
            "terminal.integrated.fontFamily": "MesloLGS NF",
            "workbench.panel.defaultLocation": "right",
            "window.zoomLevel": self.osvalue(2.5, 1.2),
            "editor.fontSize": self.osvalue(20, 14),

            # code-runner.
            "code-runner.clearPreviousOutput": True,
            "code-runner.ignoreSelection": True,
            "code-runner.saveAllFilesBeforeRun": True,
            "code-runner.showExecutionMessage": False,
            "code-runner.executorMap": {
                "python": self.osvalue("python3", "python"),
                "c": f"cmake --build build > {os.devnull} && build/dhanush",
                "cpp": f"cmake --build build > {os.devnull} && build/dhanush",
                "java": f"cmake --build target > {os.devnull} && java -cp target/CMakeFiles/JavaProject.dir/ com.package.Main"
            },

            # Formatting.
            "[python]": {"editor.defaultFormatter": "ms-python.autopep8"},
            "C_Cpp.clang_format_style": r"{BasedOnStyle: Google, IndentWidth: 4, AllowShortFunctionsOnASingleLine: Empty}",
            "[shellscript]": {"editor.defaultFormatter": "mkhl.shfmt"},
            "[jsonc]": {"editor.defaultFormatter": "esbenp.prettier-vscode"},
            "[java]": {"editor.defaultFormatter": "redhat.java"},
            "java.format.settings.url": "https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml"
        }

        settings.update(additional)

        settings_json = json.dumps(settings, indent=2)
        settings_file = (
            self.vsdir / "settings.json" if universal else ".vscode/settings.json"
        )
        Path(settings_file).write_text(settings_json)

    def bindkey_vscode(self, additional: list = []):
        """Adds vscode keybindings."""
        keybindings = [
            {
                "key": "shift+alt+down",
                "command": "editor.action.copyLinesDownAction",
                "when": "editorTextFocus && !editorReadonly",
            },
            {
                "key": "ctrl+shift+down",
                "command": "editor.action.insertCursorBelow",
                "when": "editorTextFocus"
            },
            {
                "key": "ctrl+alt+n",
                "command": "runCommands",
                "args": {
                    "commands": ["workbench.action.positionPanelRight", "code-runner.run"]
                },
            },
            {
                "key": "ctrl+shift+m",
                "command": "runCommands",
                "args": {
                    "commands": [
                        "workbench.actions.view.problems",
                        "workbench.action.positionPanelBottom",
                    ]
                },
            },
        ]

        keybindings.extend(additional)

        keybindings_json = json.dumps(keybindings, indent=2)
        settings_file = self.vsdir / "keybindings.json"
        Path(settings_file).write_text(keybindings_json)
