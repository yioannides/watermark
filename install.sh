#!/usr/bin/env bash

set -e

APP="watermark"
REPO="https://github.com/yioannides/watermark"
INSTALL_DIR="$HOME/.${APP}" 
LAUNCH_DIR="$HOME/.local/bin/${APP}" 

echo -e "Installing \033[1m${APP}\033[22m..."
sleep 1.5

mkdir -p "$HOME/.local/bin"

# determine the shell
if [[ $SHELL == */zsh ]]; then
  SHELL_RC="$HOME/.zshrc"
elif [[ $SHELL == */bash ]]; then
  SHELL_RC="$HOME/.bashrc"
else
  SHELL_RC="$HOME/.profile"
fi

if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
fi

export PATH="$HOME/.local/bin:$PATH"

# clone / update repo
if [ -d "$INSTALL_DIR" ]; then
	cd "$INSTALL_DIR"
	git pull
else
	git clone "$REPO" "$INSTALL_DIR"
	cd "$INSTALL_DIR"
fi

# set up a Python environment
if [ ! -d "venv" ]; then
  /usr/bin/python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install pydub

# create launcher
cat << EOF > "$LAUNCH_DIR"
#!/usr/bin/env bash
source "$INSTALL_DIR/venv/bin/activate"
python "$INSTALL_DIR/src/$APP.py" "\$@"
EOF

chmod +x "$LAUNCH_DIR"

echo -e "Installation complete! You can now run the script by typing:\n\033[1m$APP\033[22m (add \033[3mhelp\033[23m for usage instructions)"
