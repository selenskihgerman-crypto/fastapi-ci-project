-- Прямые заказы (без менеджеров)
SELECT
    c.customer_name,
    o.order_id
FROM
    Orders o
JOIN
    Customers c ON o.customer_id = c.customer_id
WHERE
    c.manager_id IS NULL;