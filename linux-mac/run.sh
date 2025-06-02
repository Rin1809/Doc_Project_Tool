#!/usr/bin/env bash

SCRIPT_DIR_RAW="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR_RAW}/.." && pwd)"
cd "$PROJECT_ROOT"

VENV_NAME="moitruongao"
PYTHON_EXE_IN_VENV="$VENV_NAME/bin/python"
MAIN_SCRIPT="run_app.py"

echo "==========================================================="
echo "Doc_Project_Tool Setup & Run Script for Linux/macOS"
echo "==========================================================="
echo "Project Root: $(pwd)"
echo "Virtual Environment: $VENV_NAME"
echo "Main Script: $MAIN_SCRIPT"
echo ""

PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "==========================================================="
    echo "ERROR: Python is not installed or not found in PATH."
    echo "Please install Python 3."
    echo "==========================================================="
    read -p "Press Enter to exit..."
    exit 1
fi
echo "Python installation found ($PYTHON_CMD)."
echo ""

if [ ! -d "$VENV_NAME/bin" ]; then
    echo "==========================================================="
    echo "Creating virtual environment: $VENV_NAME..."
    echo "==========================================================="
    "$PYTHON_CMD" -m venv "$VENV_NAME"
    if [ $? -ne 0 ]; then
        echo "==========================================================="
        echo "ERROR: Failed to create virtual environment."
        echo "Please check your Python installation and permissions."
        echo "==========================================================="
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "==========================================================="
    echo "Virtual environment created successfully."
    echo "==========================================================="
    echo ""
else
    echo "Virtual environment '$VENV_NAME' already exists."
    echo ""
fi

echo "==========================================================="
echo "Activating virtual environment..."
echo "==========================================================="
source "$VENV_NAME/bin/activate"
if [ $? -ne 0 ]; then
    echo "==========================================================="
    echo "ERROR: Failed to activate virtual environment."
    echo "==========================================================="
    read -p "Press Enter to exit..."
    exit 1
fi
echo "Virtual environment activated."
echo ""

echo "==========================================================="
echo "Installing dependencies from requirements.txt..."
echo "==========================================================="
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "==========================================================="
    echo "ERROR: Failed to install dependencies."
    echo "Please check requirements.txt and your internet connection."
    echo "==========================================================="
    read -p "Press Enter to exit..."
    exit 1
fi
echo "Dependencies installed successfully."
echo ""

echo "==========================================================="
echo "Running Doc_Project_Tool application..."
echo "(This terminal window will close shortly)"
echo "==========================================================="

if [ -f "$PYTHON_EXE_IN_VENV" ]; then
    nohup "$PYTHON_EXE_IN_VENV" "$MAIN_SCRIPT" > /dev/null 2>&1 &
else
    echo "==========================================================="
    echo "ERROR: Python executable not found in virtual environment."
    echo "$PYTHON_EXE_IN_VENV"
    echo "==========================================================="
    read -p "Press Enter to exit..."
    exit 1
fi

sleep 1

exit 0