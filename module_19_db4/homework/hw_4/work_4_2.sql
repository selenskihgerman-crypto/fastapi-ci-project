SELECT
    c.name AS class_name,
    AVG(late_counts.late_count) AS avg_late,
    MAX(late_counts.late_count) AS max_late,
    MIN(late_counts.late_count) AS min_late
FROM classes c
LEFT JOIN (
    SELECT
        s.class_id,
        s.id AS student_id,
        COUNT(*) AS late_count
    FROM assignments a
    JOIN grades g ON a.id = g.assignment_id
    JOIN students s ON g.student_id = s.id
    WHERE g.submitted_at > a.deadline
    GROUP BY s.class_id, s.id
) late_counts ON c.id = late_counts.class_id
GROUP BY c.id, c.name;