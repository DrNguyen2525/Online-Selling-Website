import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister
from resources.delivery import Delivery, DeliveryList, DeliveryStatus
from resources.delivery_unit import DeliveryUnit, DeliveryUnitList
from resources.shipper import Shipper, ShipperList

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'SP10'
api = Api(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWT(app, authenticate, identity)      # /auth

api.add_resource(DeliveryUnit, '/delivery_units/<int:delivery_unit_id>')
api.add_resource(DeliveryUnitList, '/delivery_units')
api.add_resource(Delivery, '/deliveries/<int:order_id>')
api.add_resource(DeliveryList, '/deliveries')
api.add_resource(DeliveryStatus, '/deliveries/<int:order_id>/status')
api.add_resource(Shipper, '/shippers/<int:shipper_id>')
api.add_resource(ShipperList, '/shippers')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=False)
