import bcrypt
from pathlib import Path

from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user

# Path to the users.txt file from Week 7
DATA_USERS_FILE = Path("DATA") / "users.txt"


def register_user(username: str, password: str, role: str = "user"):
    """
    Register a new user in the database.
    The password is stored as a bcrypt hash.
    """
    # Check if the username is already used
    existing = get_user_by_username(username)
    if existing:
        return False, "This username already exists."

    # Hash the plain password
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt).decode("utf-8")

    # Save the user with the hashed password
    insert_user(username, hashed, role)
    return True, "User registered."


def login_user(username: str, password: str):
    """
    Check if the username exists and the password is correct.
    Returns (True, message) or (False, message).
    """
    user = get_user_by_username(username)
    if not user:
        return False, "Username not found."

    # user = (id, username, password_hash, role, created_at)
    stored_hash = user[2]
    ok = bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))

    if ok:
        return True, "Login successful."
    else:
        return False, "Incorrect password."


def migrate_users_from_file():
    """
    Read old users from users.txt and add them into the users table.
    File format: username,password_hash,role(optional)
    """
    if not DATA_USERS_FILE.exists():
        print("users.txt file not found.")
        return 0

    conn = connect_database()
    cursor = conn.cursor()
    migrated = 0

    with DATA_USERS_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) < 2:
                continue

            username = parts[0]
            password_hash = parts[1]
            role = parts[2] if len(parts) >= 3 else "user"

            try:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO users (username, password_hash, role)
                    VALUES (?, ?, ?)
                    """,
                    (username, password_hash, role),
                )
                if cursor.rowcount > 0:
                    migrated += 1
            except Exception:
                # Ignore errors for a single bad line
                pass

    conn.commit()
    conn.close()
    print("Users migrated from file:", migrated)
    return migrated
