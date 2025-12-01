from app.data.db import connect_database


def get_user_by_username(username: str):
    """
    Return one user row with this username.
    If the user does not exist, return None.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def insert_user(username: str, password_hash: str, role: str = "user"):
    """
    Add a new user to the users table.
    The password must already be hashed.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role),
    )
    conn.commit()
    conn.close()
