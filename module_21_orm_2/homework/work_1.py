from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, create_engine, event
from sqlalchemy.orm import relationship, sessionmaker, joinedload, subqueryload, contains_eager
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func, and_, or_, not_
from sqlalchemy import event
from flask import Flask, request, jsonify
import csv
from io import StringIO
from datetime import datetime, timedelta

Base = declarative_base()
app = Flask(__name__)
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)


# Модели
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    books = relationship("Book", back_populates="author",
                         cascade="all, delete-orphan",
                         lazy='joined')  # Жадная подгрузка по умолчанию


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete="CASCADE"))
    author = relationship("Author", back_populates="books")
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    receipts = relationship("ReceivingBook", back_populates="book",
                            cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    average_score = Column(Numeric(3, 2))
    receipts = relationship("ReceivingBook", back_populates="student",
                            cascade="all, delete-orphan")

    # Association proxy для связи many-to-many с книгами
    books = association_proxy('receipts', 'book',
                              creator=lambda book: ReceivingBook(book=book))


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"))
    student_id = Column(Integer, ForeignKey('students.id', ondelete="CASCADE"))
    date_of_issue = Column(Date, default=datetime.now)
    date_of_return = Column(Date)

    book = relationship("Book", back_populates="receipts")
    student = relationship("Student", back_populates="receipts")


# Создание таблиц
Base.metadata.create_all(engine)


# Триггер для проверки телефона
@event.listens_for(Student, 'before_insert')
def before_student_insert(mapper, connection, target):
    if target.phone:
        import re
        pattern = r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, target.phone):
            raise ValueError("Номер телефона должен быть в формате +7(XXX)-XXX-XX-XX")