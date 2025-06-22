# Веб-сервис

from flask import Flask, jsonify, request
from models import HotelDB
import json

app = Flask(__name__)
db = HotelDB()


@app.route('/get-room', methods=['GET'])
def get_room():
    rooms = db.get_all_rooms()
    return jsonify({"rooms": [room.__dict__ for room in rooms]}), 200


@app.route('/add-room', methods=['POST'])
def add_room():
    data = request.json
    new_room = db.add_room(
        floor=data['floor'],
        guest_num=data['guestNum'],
        beds=data['beds'],
        price=data['price']
    )
    return jsonify({"rooms": [room.__dict__ for room in db.get_all_rooms()]}), 200


@app.route('/booking', methods=['POST'])
def booking():
    data = request.json
    room_id = data['roomId']

    if db.book_room(room_id):
        return jsonify({"message": "Room booked successfully"}), 200
    else:
        return jsonify({"error": "Room already booked"}), 409


if __name__ == '__main__':
    app.run(debug=True)