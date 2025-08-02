#!/bin/bash

# ╭───────────────────────────────╮
# │ ENVIRONMENT DIR/ENVRC SETUP   │
# ╰───────────────────────────────╯
if [ ! -f ".envrc" ]; then
    echo "Creating .envrc..."
    cat << EOF > .envrc
layout python3
export VIRTUAL_ENV=\$(pwd)/.venv
export PATH=\$VIRTUAL_ENV/bin:\$PATH
EOF
fi

if [ ! -d ".direnv" ]; then
    echo "Creating .direnv directory..."
    mkdir .direnv
fi

python3 -m venv .venv > /dev/null 2>&1

# Activate direnv
eval "$(direnv export bash)"
direnv allow

# ╭──────────────────────╮
# │ INSTALL DEPENDENCIES │
# ╰──────────────────────╯
pip3 install -r requirements.txt --user > /dev/null 2>&1

# ╭────────────────────────────╮
# │ PROMPT: CHOOSE FILE        │
# ╰────────────────────────────╯
ask_yes_no() {
    while true; do
        read -rp "$1 [y/n]: " yn
        case $yn in
            [Yy]* ) return 0 ;;
            [Nn]* ) return 1 ;;
            * ) echo "Please answer y or n." ;;
        esac
    done
}

DEFAULT_FILE="file.xlsx"
XLS_FILE=$DEFAULT_FILE

if ask_yes_no "Do you want to change the default Excel file ($DEFAULT_FILE)?"; then
    read -rp "Enter the full path to the Excel file: " input_file
    if [[ -f "$input_file" ]]; then
        XLS_FILE="$input_file"
    else
        echo "File not found, using the default file."
    fi
fi

# ╭──────────────────────────────╮
# │ EXPORT ENV VAR FOR APP       │
# ╰──────────────────────────────╯
export STREAMLIT_XLS_FILE="$XLS_FILE"

# ╭──────────────────────────────╮
# │ RUN STREAMLIT SILENTLY       │
# ╰──────────────────────────────╯
# Redirect errors to a file and display only useful logs
streamlit run app.py \
    --browser.gatherUsageStats=false \
    --server.headless false \
    --server.enableCORS false \
    --server.runOnSave false \
    --global.developmentMode false \
    --browser.serverAddress localhost \
    --browser.serverPort 8501 \
    2> streamlit_error.log | tee streamlit_output.log

# ╭────────────────────────────╮
# │ AUTO STOP IF BROWSER CLOSED │
# ╰────────────────────────────╯
# If the command ends (e.g., tab closed), exit.
exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo "Streamlit has been stopped (probably browser closed)."
    exit $exit_code
fi