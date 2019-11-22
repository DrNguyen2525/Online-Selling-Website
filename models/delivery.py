from db import db

import json

class DeliveryModel(db.Model):
    __tablename__ = 'deliveries'

    receiving_address = db.Column(db.String(200))
    receiver_phone = db.Column(db.String(25))
    total_cost = db.Column(db.Integer)
    expected_receving_date = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    order_id = db.Column(db.Integer, primary_key=True)
    shipper_id = db.Column(db.Integer, db.ForeignKey('shippers.id', onupdate="CASCADE", ondelete="SET NULL"))
    shipper = db.relationship('ShipperModel')
    delivery_unit_id = db.Column(db.Integer, db.ForeignKey('delivery_units.id', onupdate="CASCADE", ondelete="SET NULL"))
    delivery_unit = db.relationship('DeliveryUnitModel')

    def __init__(self, order_id, expected_receving_date, receiving_address, receiver_phone, total_cost, delivery_unit_id):
        self.order_id = order_id
        self.expected_receving_date = expected_receving_date
        self.receiving_address = receiving_address
        self.receiver_phone = receiver_phone
        self.total_cost = total_cost
        self.delivery_unit_id = delivery_unit_id
        self.status = 0

    def json(self):
        return {'order_id': self.order_id, 'delivery_unit_id': self.delivery_unit_id, 'shipper_id': self.shipper_id, 'receiving_address': self.receiving_address, 'receiver_phone': self.receiver_phone, 'total_cost': self.total_cost, 'expected_receving_date': json.dumps(self.expected_receving_date, default=str), 'status': self.status, 'success': 'true'}

    @classmethod
    def find_by_order_id(cls, order_id):
        return cls.query.filter_by(order_id=order_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
