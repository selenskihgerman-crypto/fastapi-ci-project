from flask import request, jsonify
from datetime import datetime
from app.models import db, Client, Parking, ClientParking


def init_routes(app):
    @app.route('/clients', methods=['GET'])
    def get_clients():
        clients = Client.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'surname': c.surname,
            'credit_card': c.credit_card,
            'car_number': c.car_number
        } for c in clients])

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        client = Client.query.get_or_404(client_id)
        return jsonify({
            'id': client.id,
            'name': client.name,
            'surname': client.surname,
            'credit_card': client.credit_card,
            'car_number': client.car_number
        })

    @app.route('/clients', methods=['POST'])
    def create_client():
        data = request.get_json()
        client = Client(
            name=data['name'],
            surname=data['surname'],
            credit_card=data.get('credit_card'),
            car_number=data.get('car_number')
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({'id': client.id}), 201

    @app.route('/parkings', methods=['POST'])
    def create_parking():
        data = request.get_json()
        parking = Parking(
            address=data['address'],
            opened=data.get('opened', True),
            count_places=data['count_places'],
            count_available_places=data['count_places']
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify({'id': parking.id}), 201

    @app.route('/client_parkings', methods=['POST'])
    def enter_parking():
        data = request.get_json()
        client_id = data['client_id']
        parking_id = data['parking_id']

        client = Client.query.get_or_404(client_id)
        parking = Parking.query.get_or_404(parking_id)

        if not parking.opened:
            return jsonify({'error': 'Parking is closed'}), 400

        if parking.count_available_places <= 0:
            return jsonify({'error': 'No available places'}), 400

        # Check if client is already in parking
        existing = ClientParking.query.filter_by(
            client_id=client_id,
            parking_id=parking_id,
            time_out=None
        ).first()

        if existing:
            return jsonify({'error': 'Client is already in parking'}), 400

        client_parking = ClientParking(
            client_id=client_id,
            parking_id=parking_id,
            time_in=datetime.now()
        )

        parking.count_available_places -= 1
        db.session.add(client_parking)
        db.session.commit()

        return jsonify({'id': client_parking.id}), 201

    @app.route('/client_parkings', methods=['DELETE'])
    def exit_parking():
        data = request.get_json()
        client_id = data['client_id']
        parking_id = data['parking_id']

        # Ищем активную запись о парковке
        client_parking = ClientParking.query.filter_by(
            client_id=client_id,
            parking_id=parking_id,
            time_out=None
        ).first()

        if not client_parking:
            return jsonify({'error': 'No active parking record found'}), 404

        # Получаем клиента из базы данных
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'Client not found'}), 404

        if not client.credit_card:
            return jsonify({'error': 'No credit card for payment'}), 400

        # Calculate parking time and cost (simplified)
        parking_time = datetime.now() - client_parking.time_in
        hours = parking_time.total_seconds() / 3600
        cost = hours * 50  # 50 per hour

        client_parking.time_out = datetime.now()

        parking = Parking.query.get(parking_id)
        parking.count_available_places += 1

        db.session.commit()

        return jsonify({
            'parking_time_hours': round(hours, 2),
            'cost': round(cost, 2)
        }), 200