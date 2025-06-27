@app.route('/students/upload_csv', methods=['POST'])
def upload_students_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File must be CSV"}), 400

    try:
        # Чтение CSV файла
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream, delimiter=';')

        # Подготовка данных для вставки
        students_data = []
        for row in csv_reader:
            students_data.append({
                'name': row['name'],
                'phone': row.get('phone'),
                'average_score': float(row.get('average_score', 0))
            })

        # Массовая вставка
        session = Session()
        try:
            session.bulk_insert_mappings(Student, students_data)
            session.commit()
            return jsonify({"message": f"{len(students_data)} students added"})
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500