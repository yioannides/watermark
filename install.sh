#!/usr/bin/env bash

set -e

APP="watermark"
REPO="https://gitlab.com/yioannides/watermark"
INSTALL_DIR="$HOME/.${APP}"

echo -e "\nInstalling \e[1m${APP}\e[22m..."
sleep 1.5

# Determine the shell rc file
if [[ $SHELL == */zsh ]]; then
  SHELL_RC="$HOME/.zshrc"
elif [[ $SHELL == */bash ]]; then
  SHELL_RC="$HOME/.bashrc"
else
  SHELL_RC="$HOME/.profile"
fi

# Clone or update repo
if [ -d "$INSTALL_DIR" ]; then
  cd "$INSTALL_DIR"
  git pull
else
  git clone "$REPO" "$INSTALL_DIR"
fi

pip3 install --user --upgrade pydub audioop-lts

# Add alias to shell rc if not present
ALIAS_CMD="alias ${APP}='python3 \$HOME/.${APP}/src/${APP}.py \"\$@\"'"

if ! grep -Fxq "$ALIAS_CMD" "$SHELL_RC" 2>/dev/null; then
  echo "$ALIAS_CMD" >> "$SHELL_RC"
fi

echo -e "\n------\nInstallation complete! You can now run the script by typing:\n\e[1m$APP\e[22m (type \e[3m-h\e[23m or \e[3m--help\e[23m for usage instructions)\n"
