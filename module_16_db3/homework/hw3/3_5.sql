SELECT DISTINCT o.ship
FROM outcomes o
JOIN battles b ON o.battle = b.name
WHERE o.result = 'damaged' AND EXISTS (
    SELECT 1
    FROM outcomes o2
    JOIN battles b2 ON o2.battle = b2.name
    WHERE o2.ship = o.ship AND b2.date > b.date
);