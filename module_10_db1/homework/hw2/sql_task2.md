# Отчет по исследованию продаж телефонов

## 1. Телефоны какого цвета чаще всего покупают?

```sql
SELECT p.color, COUNT(*) as sales_count
FROM table_phones p
JOIN table_checkout c ON p.id = c.phone_id
GROUP BY p.color
ORDER BY sales_count DESC
LIMIT 1;
