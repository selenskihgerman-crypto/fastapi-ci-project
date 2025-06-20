def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    cursor.execute("""
        INSERT INTO table_birds (bird_name, date_time)
        VALUES (?, ?)
    """, (bird_name, date_time))


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    cursor.execute("""
        SELECT EXISTS(
            SELECT 1 
            FROM table_birds 
            WHERE bird_name = ?
            LIMIT 1
        )
    """, (bird_name,))
    return cursor.fetchone()[0] == 1