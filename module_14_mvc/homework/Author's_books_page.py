@app.route('/author/<author_name>')
def get_author_books(author_name):
    author = Author.query.filter_by(name=author_name).first()

    if not author:
        return render_template('author_books.html',
                               author_name=author_name,
                               books=[])

    books = Book.query.filter_by(author_id=author.id).all()

    # Увеличиваем счетчики просмотров
    for book in books:
        book.views += 1
    db.session.commit()

    return render_template('author_books.html',
                           author_name=author_name,
                           books=books)