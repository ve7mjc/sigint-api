import sys
from pathlib import Path
from dotenv import load_dotenv


def add_parent_to_path():

    script_folder = Path(__file__).resolve().parent
    parent_folder = script_folder.parent

    # Add the parent folder to the environment path
    if str(parent_folder) not in sys.path:
        sys.path.insert(0, str(parent_folder))  # Prepend to the path for priority


# simply importing this module is sufficient
load_dotenv()
add_parent_to_path()