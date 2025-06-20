IVAN_SOVIN_SALARY = 100000


def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    # Получаем текущую зарплату сотрудника
    cursor.execute("""
        SELECT salary 
        FROM table_effective_manager 
        WHERE name = ?
    """, (name,))
    result = cursor.fetchone()

    if not result:
        return

    current_salary = result[0]
    new_salary = current_salary * 1.1

    if new_salary > IVAN_SOVIN_SALARY:
        # Увольняем сотрудника
        cursor.execute("""
            DELETE FROM table_effective_manager 
            WHERE name = ?
        """, (name,))
    else:
        # Повышаем зарплату
        cursor.execute("""
            UPDATE table_effective_manager 
            SET salary = ? 
            WHERE name = ?
        """, (new_salary, name))