#!/usr/bin/env bash

set -e

APP="watermark"
REPO="https://github.com/yioannides/watermark"
INSTALL_DIR="$HOME/.${APP}"

echo -e "Installing \033[1m${APP}\033[22m..."
sleep 1.5

mkdir -p "$HOME/.local/bin"

# Determine shell rc file
if [[ $SHELL == */zsh ]]; then
  SHELL_RC="$HOME/.zshrc"
elif [[ $SHELL == */bash ]]; then
  SHELL_RC="$HOME/.bashrc"
else
  SHELL_RC="$HOME/.profile"
fi

# Add ~/.local/bin to PATH if not present
if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
fi

export PATH="$HOME/.local/bin:$PATH"

# Clone or update repo
if [ -d "$INSTALL_DIR" ]; then
  cd "$INSTALL_DIR"
  git pull
else
  git clone "$REPO" "$INSTALL_DIR"
  cd "$INSTALL_DIR"
fi

# Setup Python environment
if [ ! -d "venv" ]; then
  /usr/bin/python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip pydub

echo -e "\nInstallation complete! You can now run the script by typing:\n\033[1m$APP\033[22m (add \033[3mhelp\033[23m for usage instructions)"
