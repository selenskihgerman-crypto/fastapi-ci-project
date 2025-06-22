-- Покупатели без заказов
SELECT
    c.customer_name
FROM
    Customers c
LEFT JOIN
    Orders o ON c.customer_id = o.customer_id
WHERE
    o.order_id IS NULL;