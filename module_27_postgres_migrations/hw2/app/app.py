from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, ARRAY, JSON, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.mutable import MutableList
import requests
import random
import json

app = Flask(__name__)
app.data_initialized = False

# Database configuration
DATABASE_URL = "postgresql://skillbox_user:password@localhost:5432/skillbox_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models
class Coffee(Base):
    __tablename__ = 'coffee'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(200))
    description = Column(String(200))
    reviews = Column(MutableList.as_mutable(ARRAY(String)))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    coffee = relationship("Coffee")


def initialize_data():
    if app.data_initialized:
        return

    session = SessionLocal()
    try:
        if session.query(Coffee).first():
            return

        print("Получаем данные о кофе...")
        coffee_response = requests.get('https://dummyjson.com/products/search?q=coffee')
        coffee_data = coffee_response.json()

        coffee_products = []
        for product in coffee_data['products'][:3]:
            reviews = [review.get('comment', '') for review in product.get('reviews', [])[:2]]
            coffee = Coffee(
                title=product['title'],
                category=product['category'],
                description=product['description'][:200],
                reviews=reviews
            )
            coffee_products.append(coffee)

        session.add_all(coffee_products)
        session.commit()

        print("Получаем данные о пользователях...")
        users_response = requests.get('https://dummyjson.com/users?limit=5')
        users_data = users_response.json()

        for user_data in users_data['users']:
            user = User(
                name=f"{user_data['firstName']} {user_data['lastName']}",
                address={
                    'address': user_data['address']['address'],
                    'city': user_data['address']['city'],
                    'state': user_data['address']['state'],
                    'country': user_data['address']['country']
                },
                coffee_id=random.choice([c.id for c in coffee_products])
            )
            session.add(user)

        session.commit()
        app.data_initialized = True
        print("Тестовые данные созданы успешно!")

    except Exception as e:
        session.rollback()
        print(f"Ошибка создания данных: {e}")
    finally:
        session.close()


@app.before_request
def before_first_request():
    if not app.data_initialized:
        initialize_data()


# Routes
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    session = SessionLocal()
    try:
        coffee_id = data.get('coffee_id')
        if not coffee_id:
            coffee = session.query(Coffee).order_by(text('RANDOM()')).first()
            coffee_id = coffee.id

        user = User(
            name=data['name'],
            address=data.get('address', {}),
            coffee_id=coffee_id
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return jsonify({
            'id': user.id,
            'name': user.name,
            'address': user.address,
            'coffee': {
                'id': user.coffee.id,
                'title': user.coffee.title,
                'category': user.coffee.category
            }
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@app.route('/search_coffee')
def search_coffee():
    query = request.args.get('q', '')
    session = SessionLocal()
    try:
        results = session.query(Coffee).filter(
            text("to_tsvector('english', title || ' ' || description) @@ plainto_tsquery('english', :query)")
        ).params(query=query).all()

        return jsonify([{
            'id': coffee.id,
            'title': coffee.title,
            'category': coffee.category,
            'description': coffee.description
        } for coffee in results])
    finally:
        session.close()


@app.route('/unique_notes')
def unique_notes():
    session = SessionLocal()
    try:
        all_reviews = session.query(Coffee.reviews).all()
        flat_reviews = [note for sublist in all_reviews for note in sublist[0]]
        unique_notes = list(set(flat_reviews))
        return jsonify({'unique_notes': unique_notes})
    finally:
        session.close()


@app.route('/users_by_country')
def users_by_country():
    country = request.args.get('country', '')
    session = SessionLocal()
    try:
        users = session.query(User).filter(
            User.address['country'].astext == country
        ).all()

        return jsonify([{
            'id': user.id,
            'name': user.name,
            'address': user.address,
            'coffee': user.coffee.title if user.coffee else None
        } for user in users])
    finally:
        session.close()


@app.route('/')
def hello():
    return "Flask app with PostgreSQL is working!"


if __name__ == '__main__':
    app.run(debug=True, port=5000)