#!/bin/bash
cd "$(dirname "$0")" || exit
python3 -m venv venv || exit
source venv/bin/activate || exit
pip install -r requirements.txt || exit
python main.py
