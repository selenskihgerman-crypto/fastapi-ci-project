SELECT DISTINCT s.name
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN assignments a ON g.assignment_id = a.id
JOIN (
    SELECT t.id
    FROM teachers t
    JOIN assignments a ON t.id = a.teacher_id
    JOIN grades g ON a.id = g.assignment_id
    GROUP BY t.id
    ORDER BY AVG(g.grade) DESC
    LIMIT 1
) easiest_teacher ON a.teacher_id = easiest_teacher.id;