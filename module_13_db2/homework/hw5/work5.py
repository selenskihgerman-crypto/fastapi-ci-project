import random


def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    # Очищаем таблицы
    cursor.execute("DELETE FROM uefa_commands")
    cursor.execute("DELETE FROM uefa_draw")

    # Генерируем команды
    commands = []
    command_id = 1

    # Сильные команды (1 на группу)
    strong_teams = [f"StrongTeam_{i}" for i in range(1, number_of_groups + 1)]
    for team in strong_teams:
        commands.append((command_id, team, f"Country_{command_id}", "strong"))
        command_id += 1

    # Средние команды (2 на группу)
    medium_teams = [f"MediumTeam_{i}" for i in range(1, 2 * number_of_groups + 1)]
    for team in medium_teams:
        commands.append((command_id, team, f"Country_{command_id}", "medium"))
        command_id += 1

    # Слабые команды (1 на группу)
    weak_teams = [f"WeakTeam_{i}" for i in range(1, number_of_groups + 1)]
    for team in weak_teams:
        commands.append((command_id, team, f"Country_{command_id}", "weak"))
        command_id += 1

    # Вставляем команды в таблицу
    cursor.executemany("""
        INSERT INTO uefa_commands (command_id, command_name, country, level)
        VALUES (?, ?, ?, ?)
    """, commands)

    # Жеребьевка команд по группам
    draw_data = []

    # Перемешиваем команды каждого уровня
    strong_ids = [i for i in range(1, number_of_groups + 1)]
    medium_ids = [i for i in range(number_of_groups + 1, 3 * number_of_groups + 1)]
    weak_ids = [i for i in range(3 * number_of_groups + 1, 4 * number_of_groups + 1)]

    random.shuffle(strong_ids)
    random.shuffle(medium_ids)
    random.shuffle(weak_ids)

    # Распределяем команды по группам
    for group in range(1, number_of_groups + 1):
        # Сильная команда
        draw_data.append((strong_ids.pop(), group))

        # Две средние команды
        draw_data.append((medium_ids.pop(), group))
        draw_data.append((medium_ids.pop(), group))

        # Слабая команда
        draw_data.append((weak_ids.pop(), group))

    # Вставляем данные жеребьевки
    cursor.executemany("""
        INSERT INTO uefa_draw (command_id, group_id)
        VALUES (?, ?)
    """, draw_data)