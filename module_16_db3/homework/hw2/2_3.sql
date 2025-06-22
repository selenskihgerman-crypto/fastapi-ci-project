-- Заказы с разными городами продавца и покупателя
SELECT
    o.order_id,
    s.seller_name,
    c.customer_name
FROM
    Orders o
JOIN
    Customers c ON o.customer_id = c.customer_id
JOIN
    Sellers s ON o.seller_id = s.seller_id
WHERE
    s.city != c.city;