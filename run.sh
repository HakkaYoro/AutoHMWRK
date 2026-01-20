#!/bin/bash
set -e

# Change directory to the script's location
cd "$(dirname "$0")"

echo "=== AutoHMWRK Launcher ==="

# Define required python version
PYTHON_CMD="python3.11"

# Check if Python 3.11 is installed
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "ERROR: $PYTHON_CMD no está instalado."
    echo "Este programa requiere Python 3.11 específicamente."
    if [ -f /etc/arch-release ]; then
        echo "En Arch Linux, puedes instalarlo desde AUR (por ejemplo, 'yay -S python311') o compilarlo."
    else
        echo "Por favor instale Python 3.11 en su sistema."
    fi
    exit 1
fi

# Check for required system packages (Arch Linux specific check as requested)
if [ -f /etc/arch-release ]; then
    echo "Checking for system dependencies..."
    PACKAGES_NEEDED=""
    # Simplified check, not blocking
    if ! command -v pip &> /dev/null; then 
        echo "Advertencia: 'pip' no encontrado en el sistema base (se usará el del venv si existe)."
    fi
fi

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment using $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv
    touch venv/.requirements_state
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Validate python version inside venv check
VENV_PYTHON_VERSION=$(python --version)
echo "Using: $VENV_PYTHON_VERSION"

# Smart Install: Check if requirements changed or packages missing
# We use a simple marker file technique or pip freeze comparison.
# Logic: If requirements.txt is newer than venv/.requirements_state, install.
# OR if simple check of a core package fails.

NEEDS_INSTALL=false

if [ requirements.txt -nt venv/.requirements_state ]; then
    NEEDS_INSTALL=true
else
    # Quick check if packages are actually importable/installed
    if ! python -c "import FreeSimpleGUI, openai, dotenv" &> /dev/null; then
        NEEDS_INSTALL=true
    fi
fi

if [ "$NEEDS_INSTALL" = true ]; then
    echo "Installing/Updating dependencies..."
    
    # Uninstall conflicting PySimpleGUI if present (from previous bad installs)
    if pip show PySimpleGUI &> /dev/null; then
        echo "Uninstalling conflicting PySimpleGUI..."
        pip uninstall -y PySimpleGUI
    fi
    
    pip install -r requirements.txt
    touch venv/.requirements_state
else
    echo "Dependencies appear to be up to date. Skipping install."
fi

# Run the application
echo "Starting AutoHMWRK..."
python main.py
