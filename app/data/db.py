from pathlib import Path
import sqlite3

# Folder for CSV files and the database file
DATA_DIR = Path("DATA")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Path to the SQLite database file
DB_PATH = DATA_DIR / "intelligence_platform.db"


def connect_database(db_path: Path = DB_PATH):
    """
    Open a connection to the SQLite database.
    The file is created if it does not exist.
    """
    return sqlite3.connect(str(db_path))
