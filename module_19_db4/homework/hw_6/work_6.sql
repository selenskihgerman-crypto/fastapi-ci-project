SELECT AVG(g.grade) AS avg_reading_study_grade
FROM grades g
WHERE g.assignment_id IN (
    SELECT a.id
    FROM assignments a
    WHERE a.description LIKE '%прочитать%'
       OR a.description LIKE '%выучить%'
       OR a.description LIKE '%изучить%'
);