import sqlite3

def analyze_tables():
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()
        
        # 1. Количество записей в каждой таблице
        print("Количество записей в таблицах:")
        for table in ['table_1', 'table_2', 'table_3']:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} записей")
        
        # 2. Уникальные записи в table_1 (которые не встречались в других таблицах)
        cursor.execute("""
            SELECT COUNT(DISTINCT t1.value)
            FROM table_1 t1
            WHERE NOT EXISTS (
                SELECT 1 FROM table_2 t2 WHERE t2.value = t1.value
            ) AND NOT EXISTS (
                SELECT 1 FROM table_3 t3 WHERE t3.value = t1.value
            )
        """)
        unique_count = cursor.fetchone()[0]
        print(f"\nУникальных записей в table_1 (не встречаются в других таблицах): {unique_count}")
        
        # 3. Записи из table_1, которые встречаются в table_2
        cursor.execute("""
            SELECT COUNT(DISTINCT t1.value)
            FROM table_1 t1
            WHERE EXISTS (
                SELECT 1 FROM table_2 t2 WHERE t2.value = t1.value
            )
        """)
        in_table2_count = cursor.fetchone()[0]
        print(f"\nЗаписей из table_1, встречающихся в table_2: {in_table2_count}")
        
        # 4. Записи из table_1, которые встречаются и в table_2, и в table_3
        cursor.execute("""
            SELECT COUNT(DISTINCT t1.value)
            FROM table_1 t1
            WHERE EXISTS (
                SELECT 1 FROM table_2 t2 WHERE t2.value = t1.value
            ) AND EXISTS (
                SELECT 1 FROM table_3 t3 WHERE t3.value = t1.value
            )
        """)
        in_both_count = cursor.fetchone()[0]
        print(f"\nЗаписей из table_1, встречающихся и в table_2, и в table_3: {in_both_count}")

analyze_tables()
