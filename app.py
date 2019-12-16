import os

from flask import Flask, session, render_template, request, redirect, g, url_for
from flask_restful import Api
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister
from resources.delivery import Delivery, DeliveryList, DeliveryShipper, DeliveryStatus
from resources.delivery_unit import DeliveryUnit, DeliveryUnitList
from resources.shipper import Shipper, ShipperList

from service_explorer import account_service, delivery_service, order_service

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
api.add_resource(Delivery, '/deliveries/<int:order_id>')
api.add_resource(DeliveryList, '/deliveries')
api.add_resource(DeliveryShipper, '/deliveries/<int:order_id>/shipper')
api.add_resource(DeliveryStatus, '/deliveries/<int:order_id>/status')
api.add_resource(Shipper, '/shippers/<int:shipper_id>')
api.add_resource(ShipperList, '/shippers')

api.add_resource(UserRegister, '/register')

@app.route('/')
def index():
    return redirect(account_service + "/requirelogin" + "?url=" + delivery_service)

@app.route('/protected')
def protected():
    if g.user_id:
        return render_template('protected.html')

    return redirect(account_service + "/requirelogin" + "?url=" + delivery_service)

@app.route('/logout')
def logout():
    return redirect(account_service + "/logout" + "?url=" + delivery_service)

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
    return redirect(url_for('protected'))

@app.route('/getsession')
def getsession():
    if 'user_id' in session and 'session_id' in session:
        return session['user_id'] + session['session_id']

    return 'Not logged in !'

@app.route('/destroysession')
def dropsession():
    session.pop('user_id', None)
    session.pop('session_id', None)
    return 'Session destroyed.'

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=False)
