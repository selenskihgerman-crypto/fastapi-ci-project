@app.route('/books/available_by_author/<int:author_id>', methods=['GET'])
def available_books_by_author(author_id):
    session = Session()
    try:
        total = session.query(func.sum(Book.available_copies)) \
            .filter(Book.author_id == author_id) \
            .scalar()
        return jsonify({"author_id": author_id, "available_books": total or 0})
    finally:
        session.close()


@app.route('/books/unread_by_student/<int:student_id>', methods=['GET'])
def unread_books_by_student(student_id):
    session = Session()
    try:
        # Находим авторов, книги которых студент уже брал
        read_authors = session.query(Book.author_id) \
            .join(ReceivingBook) \
            .filter(ReceivingBook.student_id == student_id) \
            .distinct()

        # Находим книги этих авторов, которые студент не брал
        unread_books = session.query(Book) \
            .filter(Book.author_id.in_(read_authors)) \
            .filter(~Book.receipts.any(ReceivingBook.student_id == student_id)) \
            .all()

        result = [{"id": book.id, "title": book.title, "author": book.author.name}
                  for book in unread_books]
        return jsonify(result)
    finally:
        session.close()


@app.route('/stats/avg_books_this_month', methods=['GET'])
def avg_books_this_month():
    session = Session()
    try:
        first_day = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        avg = session.query(func.count(ReceivingBook.id)) \
            .filter(ReceivingBook.date_of_issue >= first_day) \
            .scalar()

        # Количество студентов, которые брали книги
        student_count = session.query(func.count(distinct(ReceivingBook.student_id))) \
                            .filter(ReceivingBook.date_of_issue >= first_day) \
                            .scalar() or 1

        avg = avg / student_count if student_count else 0
        return jsonify({"avg_books_per_student": round(avg, 2)})
    finally:
        session.close()


@app.route('/stats/popular_book_high_score', methods=['GET'])
def popular_book_high_score():
    session = Session()
    try:
        # Подзапрос для студентов с high score
        high_score_students = session.query(Student.id) \
            .filter(Student.average_score > 4.0) \
            .subquery()

        # Находим самую популярную книгу среди этих студентов
        popular_book = session.query(Book.id, Book.title, func.count(ReceivingBook.id).label('count')) \
            .join(ReceivingBook) \
            .filter(ReceivingBook.student_id.in_(high_score_students)) \
            .group_by(Book.id) \
            .order_by(func.count(ReceivingBook.id).desc()) \
            .first()

        if popular_book:
            return jsonify({
                "book_id": popular_book.id,
                "title": popular_book.title,
                "times_taken": popular_book.count
            })
        return jsonify({"message": "No data found"}), 404
    finally:
        session.close()


@app.route('/stats/top_readers_this_year', methods=['GET'])
def top_readers_this_year():
    session = Session()
    try:
        first_day = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        top_students = session.query(
            Student.id,
            Student.name,
            func.count(ReceivingBook.id).label('books_read')
        ) \
            .join(ReceivingBook) \
            .filter(ReceivingBook.date_of_issue >= first_day) \
            .group_by(Student.id) \
            .order_by(func.count(ReceivingBook.id).desc()) \
            .limit(10) \
            .all()

        result = [{"id": s.id, "name": s.name, "books_read": s.books_read}
                  for s in top_students]
        return jsonify(result)
    finally:
        session.close()