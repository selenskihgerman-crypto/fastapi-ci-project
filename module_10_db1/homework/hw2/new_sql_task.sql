/*3. Какой самый непопулярный цвет телефона?*/
SELECT p.color, COUNT(*) as sales_count
FROM table_phones p
JOIN table_checkout c ON p.id = c.phone_id
GROUP BY p.color
ORDER BY sales_count ASC
LIMIT 1;
