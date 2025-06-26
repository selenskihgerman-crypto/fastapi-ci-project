from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

app = Flask(__name__)

# Подключение к базе данных (SQLite в данном случае)
engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route('/books', methods=['GET'])
def get_all_books():
    session = Session()
    books = session.query(Book).all()
    session.close()

    books_list = []
    for book in books:
        books_list.append({
            'id': book.id,
            'name': book.name,
            'count': book.count,
            'release_date': str(book.release_date),
            'author_id': book.author_id
        })

    return jsonify(books_list)


@app.route('/debtors', methods=['GET'])
def get_debtors():
    session = Session()
    debtors = session.query(ReceivingBook, Student).join(
        Student, ReceivingBook.student_id == Student.id
    ).filter(
        ReceivingBook.date_of_return == None,
        ReceivingBook.date_of_issue <= datetime.now() - timedelta(days=14)
    ).all()
    session.close()

    debtors_list = []
    for receiving, student in debtors:
        debtors_list.append({
            'student_id': student.id,
            'student_name': f"{student.name} {student.surname}",
            'book_id': receiving.book_id,
            'days_with_book': receiving.count_date_with_book
        })

    return jsonify(debtors_list)


@app.route('/issue_book', methods=['POST'])
def issue_book():
    data = request.json
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({'error': 'book_id and student_id are required'}), 400

    session = Session()

    # Проверяем, существует ли книга и студент
    book = session.query(Book).get(book_id)
    student = session.query(Student).get(student_id)

    if not book or not student:
        session.close()
        return jsonify({'error': 'Book or student not found'}), 404

    # Проверяем, есть ли доступные экземпляры книги
    if book.count <= 0:
        session.close()
        return jsonify({'error': 'No available copies of this book'}), 400

    # Уменьшаем количество доступных книг
    book.count -= 1

    # Создаем запись о выдаче книги
    new_issue = ReceivingBook(
        book_id=book_id,
        student_id=student_id,
        date_of_issue=datetime.now()
    )

    session.add(new_issue)
    session.commit()
    session.close()

    return jsonify({'message': 'Book issued successfully'}), 201


@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.json
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({'error': 'book_id and student_id are required'}), 400

    session = Session()

    # Находим запись о выдаче книги
    issue = session.query(ReceivingBook).filter(
        ReceivingBook.book_id == book_id,
        ReceivingBook.student_id == student_id,
        ReceivingBook.date_of_return == None
    ).first()

    if not issue:
        session.close()
        return jsonify({'error': 'No active issue record found for this book and student'}), 404

    # Находим книгу и увеличиваем количество доступных экземпляров
    book = session.query(Book).get(book_id)
    book.count += 1

    # Устанавливаем дату возврата
    issue.date_of_return = datetime.now()

    session.commit()
    session.close()

    return jsonify({'message': 'Book returned successfully'}), 200


# Дополнительный роут для поиска книг по названию
@app.route('/search_books', methods=['GET'])
def search_books():
    search_term = request.args.get('q', '')
    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400

    session = Session()
    books = session.query(Book).filter(Book.name.ilike(f'%{search_term}%')).all()
    session.close()

    books_list = []
    for book in books:
        books_list.append({
            'id': book.id,
            'name': book.name,
            'count': book.count,
            'release_date': str(book.release_date),
            'author_id': book.author_id
        })

    return jsonify(books_list)


if __name__ == '__main__':
    app.run(debug=True)