SELECT
    c.name AS class_name,
    COUNT(DISTINCT s.id) AS total_students,
    AVG(g.grade) AS avg_grade,
    COUNT(DISTINCT CASE WHEN g.grade < 60 THEN s.id END) AS failed_students,
    COUNT(DISTINCT CASE WHEN g.submitted_at > a.deadline THEN s.id END) AS late_students,
    COUNT(g.id) - COUNT(DISTINCT g.assignment_id, g.student_id) AS resubmissions
FROM classes c
LEFT JOIN students s ON c.id = s.class_id
LEFT JOIN grades g ON s.id = g.student_id
LEFT JOIN assignments a ON g.assignment_id = a.id
GROUP BY c.id, c.name;