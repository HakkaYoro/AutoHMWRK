import logging
import sys

import os

def setup_logger():
    """Configura el logger para la aplicación."""
    cwd = os.getcwd()
    log_file = os.path.join(cwd, "app.log")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )
