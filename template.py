import os
from pathlib import Path
import logging


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_of_files = [
    "src/__init__.py",
    "src/helpers.py",
    '.env',
    "requirement.text",
    "setup.py",
    "app.py",
    "research/trials.ipynb"
]

for file in list_of_files:

    
    # Create the directory if it doesn't exist
    file_path = Path(file)
    filedir, filename = os.path.split(file_path)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for {filename}")
    
    if ( not os.path.exists(file_path) or os.path.getsize(file_path) == 0 ):
        # Create the file if it doesn't exist
        with open(file_path, 'w') as f:
            pass
        logging.info(f"Created file: {file_path}")
    else:
        logging.info(f"File already exists: {file_path}")