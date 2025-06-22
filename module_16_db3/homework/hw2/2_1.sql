-- Информация о каждом заказе
SELECT
    c.customer_name AS customer,
    s.seller_name AS seller,
    o.amount,
    o.order_date
FROM
    Orders o
JOIN
    Customers c ON o.customer_id = c.customer_id
JOIN
    Sellers s ON o.seller_id = s.seller_id;