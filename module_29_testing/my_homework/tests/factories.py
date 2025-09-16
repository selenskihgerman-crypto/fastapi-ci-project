import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from app.models import db, Client, Parking

fake = Faker()


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.LazyFunction(fake.first_name)
    surname = factory.LazyFunction(fake.last_name)
    credit_card = factory.LazyAttribute(lambda x: fake.credit_card_number() if fake.boolean() else None)
    car_number = factory.LazyFunction(lambda: fake.text(max_nb_chars=10).upper())


class ParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.LazyFunction(fake.address)
    opened = factory.LazyFunction(fake.boolean)
    count_places = factory.LazyFunction(lambda: fake.random_int(min=1, max=100))
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)