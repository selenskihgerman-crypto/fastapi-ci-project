def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    # Очищаем таблицу расписания
    cursor.execute("DELETE FROM table_friendship_schedule")

    # Получаем список всех сотрудников
    cursor.execute("SELECT id FROM table_friendship_employees")
    employees = [row[0] for row in cursor.fetchall()]

    # Получаем список всех дней (366 дней)
    days = list(range(1, 367))

    # Для каждого дня определяем день недели (0-понедельник, 6-воскресенье)
    day_of_week = [(day, (day - 1) % 7) for day in days]

    # Распределяем сотрудников по дням с учетом их предпочтений
    # В этой упрощенной версии просто назначаем случайных сотрудников,
    # но в реальном решении нужно учитывать их спортивные предпочтения

    # Для демонстрации просто заполняем таблицу случайными сотрудниками
    schedule_data = []
    for day, weekday in day_of_week:
        # Выбираем 10 случайных сотрудников для смены
        shift_employees = random.sample(employees, 10)
        for emp_id in shift_employees:
            schedule_data.append((day, emp_id))

    # Вставляем данные в таблицу
    cursor.executemany("""
        INSERT INTO table_friendship_schedule (day, employee_id)
        VALUES (?, ?)
    """, schedule_data)