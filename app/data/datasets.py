import pandas as pd
from app.data.db import connect_database


def get_all_datasets():
    """
    Read all dataset metadata rows and return them as a DataFrame.
    """
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df


def insert_dataset(dataset_id, name, rows, columns, uploaded_by, upload_date):
    """
    Add one dataset metadata record to the table.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO datasets_metadata
        (dataset_id, name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (dataset_id, name, rows, columns, uploaded_by, upload_date),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def delete_dataset(record_pk_id: int):
    """
    Delete one dataset metadata record using its primary key id.
    Returns the number of deleted rows.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (record_pk_id,))
    conn.commit()
    rowcount = cursor.rowcount
    conn.close()
    return rowcount
