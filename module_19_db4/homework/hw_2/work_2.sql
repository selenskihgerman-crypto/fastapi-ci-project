SELECT s.name, AVG(g.grade) as avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.name
ORDER BY avg_grade DESC
LIMIT 10;