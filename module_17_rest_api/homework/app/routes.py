from flask_restful import Api, Resource, reqparse
from marshmallow import Schema, fields, validate, ValidationError

api = Api(app)


# Схемы для валидации и сериализации
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

    def patch(self, book_id):
        return self.put(book_id)  # В нашем случае PUT и PATCH работают одинаково

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


# Регистрация ресурсов
api.add_resource(BookListResource, '/api/books/')
api.add_resource(BookResource, '/api/books/<int:book_id>')