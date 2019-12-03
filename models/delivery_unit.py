from db import db

class DeliveryUnitModel(db.Model):
    __tablename__ = 'delivery_units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    base_fee = db.Column(db.Float)
    delivery_time = db.Column(db.Integer)

    shippers = db.relationship('ShipperModel', lazy='dynamic')
    deliveries = db.relationship('DeliveryModel', lazy='dynamic')

    def __init__(self, name, base_fee, delivery_time):
        self.name = name
        self.base_fee = base_fee
        self.delivery_time = delivery_time

    def json(self):
        return {'id': self.id, 'name': self.name, 'base_fee': self.base_fee, 'delivery_time': self.delivery_time}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_id_list(cls):
        return [value for value, in db.session.query(DeliveryUnitModel.id).all()]

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
