# Создадим форму с валидацией:
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

class BookForm(FlaskForm):
    title = StringField('Название книги', validators=[InputRequired()])
    author = StringField('Автор', validators=[InputRequired()])
    year = IntegerField('Год издания', validators=[
        InputRequired(),
        NumberRange(min=1000, max=2100)
    ])
# Обновим endpoint:
@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form():
    form = BookForm()

    if form.validate_on_submit():
        title = form.title.data
        author_name = form.author.data
        year = form.year.data

        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        new_book = Book(
            title=title,
            author_id=author.id,
            year=year,
            views=0
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('get_books'))

    return render_template('books_form.html', form=form)