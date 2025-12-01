import pandas as pd
from app.data.db import connect_database


def get_all_tickets():
    """
    Read all IT ticket rows and return them as a DataFrame.
    """
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df


def insert_ticket(ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    """
    Add one IT ticket record to the table.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO it_tickets
        (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ticket_id,
            priority,
            description,
            status,
            assigned_to,
            created_at,
            resolution_time_hours,
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_ticket_status(ticket_id: int, new_status: str):
    """
    Change the status of one ticket using the ticket_id field.
    Returns the number of updated rows.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
        (new_status, ticket_id),
    )
    conn.commit()
    rowcount = cursor.rowcount
    conn.close()
    return rowcount


def delete_ticket(ticket_id: int):
    """
    Delete one ticket using the ticket_id field.
    Returns the nцumber of deleted rows.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    rowcount = cursor.rowcount
    conn.close()
    return rowcount
