SELECT p.color, COUNT(*) as sales_count
FROM table_phones p
JOIN table_checkout c ON p.id = c.phone_id
WHERE p.color IN ('red', 'blue')
GROUP BY p.color;
