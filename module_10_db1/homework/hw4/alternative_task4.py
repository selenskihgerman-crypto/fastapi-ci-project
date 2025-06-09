# Опциональное решение с одним SQL-запросом:

import sqlite3

def analyze_incomes_single_query():
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            WITH stats AS (
                SELECT 
                    COUNT(*) as total_count,
                    SUM(CASE WHEN salary < 5000 THEN 1 ELSE 0 END) as poor_count,
                    AVG(salary) as avg_salary,
                    (SELECT salary FROM salaries ORDER BY salary LIMIT 1 OFFSET (COUNT(*)/2)) as median,
                    (SELECT SUM(salary) FROM (
                        SELECT salary FROM salaries ORDER BY salary DESC LIMIT (COUNT(*)/10)
                    )) as top10_sum,
                    (SELECT SUM(salary) FROM salaries) - (SELECT SUM(salary) FROM (
                        SELECT salary FROM salaries ORDER BY salary DESC LIMIT (COUNT(*)/10)
                    )) as rest90_sum
                FROM salaries
            )
            SELECT 
                poor_count,
                ROUND(avg_salary, 2),
                median,
                ROUND(100.0 * top10_sum / rest90_sum, 2)
            FROM stats
        """)
        
        poor, avg, median, f_coef = cursor.fetchone()
        print(f"Людей за чертой бедности: {poor}")
        print(f"Средняя зарплата: {avg} гульденов")
        print(f"Медианная зарплата: {median} гульденов")
        print(f"Коэффициент социального неравенства: {f_coef}%")

analyze_incomes_single_query()
