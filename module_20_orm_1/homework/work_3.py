from models import Base, Book, Author, Student, ReceivingBook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Создание базы данных
engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Добавление тестовых данных
authors = [
    Author(name='Лев', surname='Толстой'),
    Author(name='Фёдор', surname='Достоевский'),
    Author(name='Антон', surname='Чехов')
]
session.add_all(authors)
session.commit()

books = [
    Book(name='Война и мир', count=5, release_date=datetime(1869, 1, 1), author_id=1),
    Book(name='Анна Каренина', count=3, release_date=datetime(1877, 1, 1), author_id=1),
    Book(name='Преступление и наказание', count=4, release_date=datetime(1866, 1, 1), author_id=2),
    Book(name='Вишнёвый сад', count=2, release_date=datetime(1904, 1, 1), author_id=3)
]
session.add_all(books)
session.commit()

students = [
    Student(
        name='Иван', surname='Иванов', phone='1234567890',
        email='ivan@example.com', average_score=4.5, scholarship=True
    ),
    Student(
        name='Петр', surname='Петров', phone='0987654321',
        email='petr@example.com', average_score=3.8, scholarship=False
    ),
    Student(
        name='Сергей', surname='Сергеев', phone='1122334455',
        email='sergey@example.com', average_score=4.9, scholarship=True
    )
]
session.add_all(students)
session.commit()

# Выдача некоторых книг
receiving_books = [
    ReceivingBook(
        book_id=1, student_id=1,
        date_of_issue=datetime.now() - timedelta(days=20)
    ),
    ReceivingBook(
        book_id=3, student_id=2,
        date_of_issue=datetime.now() - timedelta(days=10),
        date_of_return=datetime.now() - timedelta(days=5)
    )
]
session.add_all(receiving_books)
session.commit()

session.close()