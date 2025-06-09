import sqlite3

def analyze_incomes():
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()
        
        # 1. Люди за чертой бедности (<5000 гульденов)
        cursor.execute("SELECT COUNT(*) FROM salaries WHERE salary < 5000")
        poor = cursor.fetchone()[0]
        print(f"Людей за чертой бедности: {poor}")
        
        # 2. Средняя зарплата
        cursor.execute("SELECT AVG(salary) FROM salaries")
        avg_salary = round(cursor.fetchone()[0], 2)
        print(f"Средняя зарплата: {avg_salary} гульденов")
        
        # 3. Медианная зарплата
        cursor.execute("""
            SELECT salary FROM salaries 
            ORDER BY salary 
            LIMIT 1 OFFSET (SELECT COUNT(*) FROM salaries) / 2
        """)
        median = cursor.fetchone()[0]
        print(f"Медианная зарплата: {median} гульденов")
        
        # 4. Коэффициент социального неравенства F = T/K
        cursor.execute("""
            SELECT ROUND(100.0 * 
                (SELECT SUM(salary) FROM (
                    SELECT salary FROM salaries 
                    ORDER BY salary DESC 
                    LIMIT (SELECT COUNT(*) FROM salaries) / 10
                )) / 
                (SELECT SUM(salary) FROM (
                    SELECT salary FROM salaries 
                    ORDER BY salary 
                    LIMIT (SELECT COUNT(*) FROM salaries) * 9 / 10
                ), 2)
        """)
        f_coefficient = cursor.fetchone()[0]
        print(f"Коэффициент социального неравенства: {f_coefficient}%")

analyze_incomes()
