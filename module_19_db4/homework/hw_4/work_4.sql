SELECT
    c.name AS class_name,
    (SELECT AVG(late_count) FROM (
        SELECT COUNT(*) AS late_count
        FROM assignments a
        JOIN grades g ON a.id = g.assignment_id
        JOIN students s ON g.student_id = s.id
        WHERE s.class_id = c.id AND g.submitted_at > a.deadline
        GROUP BY s.id
    ) late_counts) AS avg_late,
    (SELECT MAX(late_count) FROM (
        SELECT COUNT(*) AS late_count
        FROM assignments a
        JOIN grades g ON a.id = g.assignment_id
        JOIN students s ON g.student_id = s.id
        WHERE s.class_id = c.id AND g.submitted_at > a.deadline
        GROUP BY s.id
    ) late_counts) AS max_late,
    (SELECT MIN(late_count) FROM (
        SELECT COUNT(*) AS late_count
        FROM assignments a
        JOIN grades g ON a.id = g.assignment_id
        JOIN students s ON g.student_id = s.id
        WHERE s.class_id = c.id AND g.submitted_at > a.deadline
        GROUP BY s.id
    ) late_counts) AS min_late
FROM classes c;