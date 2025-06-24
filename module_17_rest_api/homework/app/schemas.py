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
        return author_schema.dump(authors, many=True)

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


# Расширенный ресурс для создания книги с возможностью создания автора
class BookWithAuthorResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('year', type=int)
        parser.add_argument('copies', type=int)

        # Поля для нового автора
        parser.add_argument('author_first_name', type=str)
        parser.add_argument('author_last_name', type=str)
        parser.add_argument('author_middle_name', type=str)

        # Или ID существующего автора
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
                # Создаем нового автора
                author_data = {
                    'first_name': args['author_first_name'],
                    'last_name': args['author_last_name'],
                    'middle_name': args['author_middle_name']
                }
                author = Author(**author_schema.load(author_data))
                db.session.add(author)
                db.session.flush()  # Получаем ID автора
                book_data['author_id'] = author.id

            validated_book_data = book_schema.load(book_data)
            book = Book(**validated_book_data)
            db.session.add(book)
            db.session.commit()

            return book_schema.dump(book), 201
        except ValidationError as err:
            db.session.rollback()
            return {'message': 'Validation error', 'errors': err.messages}, 400


# Регистрация ресурсов авторов
api.add_resource(AuthorListResource, '/api/authors/')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')
api.add_resource(BookWithAuthorResource, '/api/books-with-author/')