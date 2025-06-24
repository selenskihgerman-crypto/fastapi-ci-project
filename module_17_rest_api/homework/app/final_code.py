from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from marshmallow import Schema, fields, validate, ValidationError
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


# Модели БД
class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))

    books = relationship('Book', back_populates='author', cascade='all, delete-orphan')


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    copies = db.Column(db.Integer, default=1)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'))
    author = relationship('Author', back_populates='books')


# Схемы Marshmallow
class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str()


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    year = fields.Int()
    copies = fields.Int()
    author_id = fields.Int(required=True)

    author = fields.Nested(AuthorSchema, dump_only=True)


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# Ресурсы API
class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return book_schema.dump(book)

    def put(self, book_id):
        book = Book.query.get_or_404(book_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('year', type=int)
        parser.add_argument('copies', type=int)
        parser.add_argument('author_id', type=int)
        args = parser.parse_args()

        try:
            data = {k: v for k, v in args.items() if v is not None}
            validated_data = book_schema.load(data, partial=True)

            for key, value in validated_data.items():
                setattr(book, key, value)

            db.session.commit()
            return book_schema.dump(book)
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400

    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}, 204


class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return books_schema.dump(books)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('year', type=int)
        parser.add_argument('copies', type=int)
        parser.add_argument('author_id', type=int, required=True)
        args = parser.parse_args()

        try:
            validated_data = book_schema.load(args)
            book = Book(**validated_data)
            db.session.add(book)
            db.session.commit()
            return book_schema.dump(book), 201
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400


class AuthorResource(Resource):
    def get(self, author_id):
        author = Author.query.get_or_404(author_id)
        return {
            'author': author_schema.dump(author),
            'books': books_schema.dump(author.books)
        }

    def delete(self, author_id):
        author = Author.query.get_or_404(author_id)
        db.session.delete(author)
        db.session.commit()
        return {'message': 'Author and all their books deleted successfully'}, 204


class AuthorListResource(Resource):
    def get(self):
        authors = Author.query.all()
        return authors_schema.dump(authors)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('middle_name', type=str)
        args = parser.parse_args()

        try:
            validated_data = author_schema.load(args)
            author = Author(**validated_data)
            db.session.add(author)
            db.session.commit()
            return author_schema.dump(author), 201
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400


class BookWithAuthorResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('year', type=int)
        parser.add_argument('copies', type=int)

        parser.add_argument('author_first_name', type=str)
        parser.add_argument('author_last_name', type=str)
        parser.add_argument('author_middle_name', type=str)
        parser.add_argument('author_id', type=int)

        args = parser.parse_args()

        if not args['author_id'] and not (args['author_first_name'] and args['author_last_name']):
            return {
                'message': 'Either author_id or author_first_name and author_last_name are required'
            }, 400

        try:
            book_data = {
                'title': args['title'],
                'year': args['year'],
                'copies': args['copies']
            }

            if args['author_id']:
                book_data['author_id'] = args['author_id']
            else:
                author_data = {
                    'first_name': args['author_first_name'],
                    'last_name': args['author_last_name'],
                    'middle_name': args['author_middle_name']
                }
                author = Author(**author_schema.load(author_data))
                db.session.add(author)
                db.session.flush()
                book_data['author_id'] = author.id

            validated_book_data = book_schema.load(book_data)
            book = Book(**validated_book_data)
            db.session.add(book)
            db.session.commit()

            return book_schema.dump(book), 201
        except ValidationError as err:
            db.session.rollback()
            return {'message': 'Validation error', 'errors': err.messages}, 400


# Регистрация ресурсов
api.add_resource(BookListResource, '/api/books/')
api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(AuthorListResource, '/api/authors/')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')
api.add_resource(BookWithAuthorResource, '/api/books-with-author/')

# Создание таблиц
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)