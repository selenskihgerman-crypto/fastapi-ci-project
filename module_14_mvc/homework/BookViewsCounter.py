# Добавим endpoint для страницы книги:

@app.route('/books/<int:book_id>')
def get_book(book_id):
    book = Book.query.get(book_id)

    if not book:
        return "Книга не найдена", 404

    # Увеличиваем счетчик просмотров
    book.views += 1
    db.session.commit()

    return render_template('book.html', book=book)