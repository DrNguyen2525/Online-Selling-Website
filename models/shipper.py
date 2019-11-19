from db import db

class ShipperModel(db.Model):
    __tablename__ = 'shippers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(15))

    delivery_unit_id = db.Column(db.Integer, db.ForeignKey('delivery_units.id'))
    delivery_unit = db.relationship('DeliveryUnitModel')
    deliveries = db.relationship('DeliveryModel', lazy='dynamic')

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def json(self):
        return {'name': self.name, 'phone': self.phone}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
