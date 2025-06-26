SELECT t.name
FROM teachers t
JOIN assignments a ON t.id = a.teacher_id
JOIN grades g ON a.id = g.assignment_id
GROUP BY t.id, t.name
ORDER BY AVG(g.grade) ASC
LIMIT 1;