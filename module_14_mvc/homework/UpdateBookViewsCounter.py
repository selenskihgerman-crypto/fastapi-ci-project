# Обновим endpoint списка книг:

@app.route('/books')
def get_books():
    books = Book.query.all()

    # Увеличиваем счетчики просмотров
    for book in books:
        book.views += 1
    db.session.commit()

    return render_template('books.html', books=books)