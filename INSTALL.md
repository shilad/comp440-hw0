# Installing the course tools

Once, before the first assignment. Everything in this course runs in a terminal: Terminal on
macOS, a shell on Linux, and on Windows the Ubuntu terminal inside WSL2.

**Windows.** Install WSL2 with Ubuntu from the Microsoft Store and reboot (if it refuses,
enable virtualization in your firmware). Do everything below inside the Ubuntu terminal, and
keep your repos under your Ubuntu home, not `/mnt/c/...`. PowerShell, cmd, and Git Bash are
not supported.

1. **git** (macOS: `xcode-select --install`; Ubuntu: `sudo apt install git`), then:

   ```
   git config --global user.name "Your Name"
   git config --global user.email "you@macalester.edu"
   ```

2. **GitHub CLI** from https://cli.github.com, then `gh auth login`. GitHub no longer accepts
   account passwords, so this is how `git clone` and `git push` authenticate.
3. **uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then open a new terminal.
4. **Claude Code**: `curl -fsSL https://claude.ai/install.sh | bash`, then run `claude` and log
   in **[DECIDE: which Claude account students use]**.
5. **VS Code**, with the WSL extension on Windows. Turn off any AI autocomplete; some
   assignments have solo parts.

You are done when `git --version`, `gh auth status`, `uv --version`, and `claude --version`
all answer, and `claude` opens logged in. A command that is "not found" right after installing
usually needs a new terminal.
