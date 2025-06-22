# Модель данных

from dataclasses import dataclass


@dataclass
class Room:
    roomId: int
    floor: int
    guestNum: int
    beds: int
    price: int


class HotelDB:
    def __init__(self):
        self.rooms = [
            Room(1, 2, 1, 1, 2000),
            Room(2, 1, 2, 1, 2500)
        ]
        self.booked_rooms = set()

    def get_all_rooms(self):
        return [room for room in self.rooms if room.roomId not in self.booked_rooms]

    def add_room(self, floor, guest_num, beds, price):
        new_id = max(room.roomId for room in self.rooms) + 1 if self.rooms else 1
        new_room = Room(new_id, floor, guest_num, beds, price)
        self.rooms.append(new_room)
        return new_room

    def book_room(self, room_id):
        if room_id in self.booked_rooms:
            return False
        self.booked_rooms.add(room_id)
        return True