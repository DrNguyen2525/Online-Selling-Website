import os
import requests

from flask import Flask, session, render_template, request, redirect, g, url_for
from flask_restful import Api
from flask_cors import CORS
from requests.exceptions import HTTPError

from security import authenticate, identity
from resources.user import UserRegister
from resources.delivery import Delivery, DeliveryList, DeliveryShipper, DeliveryStatus
from resources.delivery_unit import DeliveryUnit, DeliveryUnitList, DeliveryUnitShipper, DeliveryUnitDelivery
from resources.shipper import Shipper, ShipperList

from service_explorer import account_service, delivery_service, delivery_frontend

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True
app.secret_key = os.urandom(16)
api = Api(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()

api.add_resource(DeliveryUnit, '/delivery_units/<int:delivery_unit_id>')
api.add_resource(DeliveryUnitList, '/delivery_units')
api.add_resource(DeliveryUnitShipper, '/delivery_units/<int:delivery_unit_id>/shippers')
api.add_resource(DeliveryUnitDelivery, '/delivery_units/<int:delivery_unit_id>/deliveries')

api.add_resource(Delivery, '/deliveries/<int:order_id>')
api.add_resource(DeliveryList, '/deliveries')
api.add_resource(DeliveryShipper, '/deliveries/<int:order_id>/shipper')
api.add_resource(DeliveryStatus, '/deliveries/<int:order_id>/status')

api.add_resource(Shipper, '/shippers/<int:shipper_id>')
api.add_resource(ShipperList, '/shippers')

api.add_resource(UserRegister, '/register')

@app.route('/')
def index():
    if g.user_id and g.session_id:
        try:
            response = requests.get(account_service + '/api/getsession/' + g.session_id)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}.')
            return response.json(), response.status_code
        except Exception as err:
            print(f'Other error occurred: {err}.')
            return {'message': 'An error occurred.'}, 500
        else:
            if response.json() == 'yes':
                return redirect(delivery_frontend)

    return redirect(account_service + '/requirelogin?url=' + delivery_service)

@app.route('/logout')
def logout():
    return redirect(account_service + '/logout?url=' + delivery_service)

@app.before_request
def before_request():
    g.user_id = None
    g.session_id = None
    if 'user_id' in session and 'session_id' in session:
        g.user_id = session['user_id']
        g.session_id = session['session_id']

@app.route('/setsession')
def setsession():
    session['user_id'] = request.args.get('user_id')
    session['session_id'] = request.args.get('session_id')
    return redirect(delivery_frontend)

@app.route('/getsession')
def getsession():
    if 'user_id' in session and 'session_id' in session:
        return {'user_id': '{}'.format(session['user_id']), 'session_id': '{}'.format(session['session_id'])}

    return {'message': 'Not logged in.'}

@app.route('/destroysession')
def dropsession():
    session.pop('user_id', None)
    session.pop('session_id', None)
    return redirect(account_service)

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=False)
