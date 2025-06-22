SELECT c.class
FROM classes c
LEFT JOIN ships s ON c.class = s.class
GROUP BY c.class
HAVING COUNT(DISTINCT s.name) = 2 OR COUNT(DISTINCT s.name) = 0;