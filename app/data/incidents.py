import pandas as pd
from app.data.db import connect_database


def insert_incident(incident_id, timestamp, severity, category, status, description):
    """
    Add one cyber incident to the table.
    Values should match the CSV format.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cyber_incidents
        (incident_id, timestamp, severity, category, status, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (incident_id, timestamp, severity, category, status, description),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_incidents():
    """
    Read all cyber incidents and return them as a DataFrame.
    This is useful for analysis or for the dashboard.
    """
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df


def update_incident_status(incident_pk_id: int, new_status: str):
    """
    Change the status of one incident using its primary key id.
    Returns the number of updated rows.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_pk_id),
    )
    conn.commit()
    rowcount = cursor.rowcount
    conn.close()
    return rowcount


def delete_incident(incident_pk_id: int):
    """
    Remove one incident from the table using its primary key id.
    Returns the number of deleted rows.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_pk_id,))
    conn.commit()
    rowcount = cursor.rowcount
    conn.close()
    return rowcount
