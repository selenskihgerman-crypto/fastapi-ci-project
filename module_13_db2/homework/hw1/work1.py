def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    cursor.execute("""
        SELECT COUNT(*) 
        FROM table_truck_with_vaccine 
        WHERE truck_number = ? 
        AND (temperature_celsius NOT BETWEEN -20 AND -16)
    """, (truck_number,))
    count = cursor.fetchone()[0]
    return count >= 3