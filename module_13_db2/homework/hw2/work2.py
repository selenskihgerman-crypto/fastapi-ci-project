import csv


def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # пропускаем заголовок
        wrong_fees = [(row[0], row[1]) for row in reader]

    cursor.executemany("""
        DELETE FROM table_fees 
        WHERE truck_number = ? AND timestamp = ?
    """, wrong_fees)