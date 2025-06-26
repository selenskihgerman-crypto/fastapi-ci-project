SELECT s.name
FROM students s
WHERE s.id IN (
    SELECT g.student_id
    FROM grades g
    WHERE g.assignment_id IN (
        SELECT a.id
        FROM assignments a
        WHERE a.teacher_id = (
            SELECT t.id
            FROM teachers t
            JOIN assignments a ON t.id = a.teacher_id
            JOIN grades g ON a.id = g.assignment_id
            GROUP BY t.id
            ORDER BY AVG(g.grade) DESC
            LIMIT 1
        )
    )
);