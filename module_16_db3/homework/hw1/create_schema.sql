-- Создание таблицы Customers (Покупатели)
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city TEXT NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES Managers(manager_id) ON DELETE SET NULL
);

-- Создание таблицы Managers (Менеджеры)
CREATE TABLE Managers (
    manager_id INTEGER PRIMARY KEY,
    manager_name TEXT NOT NULL,
    city TEXT NOT NULL
);

-- Создание таблицы Sellers (Продавцы)
CREATE TABLE Sellers (
    seller_id INTEGER PRIMARY KEY,
    seller_name TEXT NOT NULL,
    city TEXT NOT NULL
);

-- Создание таблицы Orders (Заказы)
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id) ON DELETE RESTRICT
);