# Задание 1.
from flask import Flask, render_template, request, redirect, url_for
from models import db, Book, Author


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form():
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.form.get('title')
        author_name = request.form.get('author')
        year = request.form.get('year')

        # Находим или создаем автора
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        # Создаем новую книгу
        new_book = Book(
            title=title,
            author_id=author.id,
            year=year,
            views=0  # Инициализируем счетчик просмотров
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('get_books'))

    return render_template('books_form.html')