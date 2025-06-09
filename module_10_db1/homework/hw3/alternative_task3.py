# Альтернативная версия с использованием INTERSECT:

import sqlite3

def analyze_tables_intersect():
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()
        
        # 1. Количество записей в каждой таблице (остается таким же)
        
        # 2. Уникальные записи в table_1 (альтернативный вариант)
        cursor.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT DISTINCT value FROM table_1
                EXCEPT
                SELECT value FROM table_2
                EXCEPT
                SELECT value FROM table_3
            )
        """)
        
        # 3. Записи из table_1 в table_2 (альтернативный вариант)
        cursor.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT DISTINCT value FROM table_1
                INTERSECT
                SELECT value FROM table_2
            )
        """)
        
        # 4. Записи из table_1 в table_2 и table_3 (альтернативный вариант)
        cursor.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT DISTINCT value FROM table_1
                INTERSECT
                SELECT value FROM table_2
                INTERSECT
                SELECT value FROM table_3
            )
        """)

# analyze_tables_intersect()
