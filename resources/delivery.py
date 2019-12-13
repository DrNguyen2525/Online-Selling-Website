import random

from flask_restful import Resource, reqparse
from datetime import datetime, timedelta

from models.delivery import DeliveryModel
from models.delivery_unit import DeliveryUnitModel
from models.shipper import ShipperModel

class Delivery(Resource):
    create_parser = reqparse.RequestParser()
    create_parser.add_argument('receiving_address',
                               type=str,
                               required=True,
                               )
    create_parser.add_argument('receiver_phone',
                               type=str,
                               required=True,
                               )
    create_parser.add_argument('total_cost',
                               type=float,
                               required=True,
                               help="This field cannot be left blank and must be a float number"
                               )
    create_parser.add_argument('delivery_unit_id',
                               type=int,
                               required=False,
                               help="This field must be an integer"
                               )

    shipper_update_parser = reqparse.RequestParser()
    shipper_update_parser.add_argument('shipper_id',
                                       type=int,
                                       required=False,
                                       help="This field cannot be left blank and must be an integer"
                                       )

    status_update_parser = reqparse.RequestParser()
    status_update_parser.add_argument('status',
                                      type=str,
                                      required=True,
                                      choices=('Pending', 'Confirmed', 'Shipping', 'Shipped', 'Canceled'),
                                      help="{error_msg}. Only 'Pending', 'Confirmed', 'Shipping', 'Shipped', 'Canceled' are available"
    )

    def get(self, order_id):
        delivery = DeliveryModel.find_by_order_id(order_id)
        if delivery:
            return delivery.json()
        return {'message': 'Delivery not found.', 'success': 'false'}, 404

    def post(self, order_id):
        if DeliveryModel.find_by_order_id(order_id):
            return {'message': f'A delivery with order_id {order_id} already exists.', 'success': 'false'}, 400

        data = Delivery.create_parser.parse_args()

        if data['delivery_unit_id'] or data['delivery_unit_id'] is not None:
            delivery_unit = DeliveryUnitModel.find_by_id(data['delivery_unit_id'])
            if delivery_unit is None:
                return {'message': 'Delivery unit not found', 'success': 'false'}, 400
        else:
            delivery_unit = DeliveryUnitModel.find_by_id(random.choice(DeliveryUnitModel.get_id_list()))
            data['delivery_unit_id'] = delivery_unit.id

        expected_receving_date = datetime.today() + timedelta(days=delivery_unit.delivery_time)

        delivery = DeliveryModel(order_id, expected_receving_date, datetime.today(), datetime.today(), **data)

        try:
            delivery.save_to_db()
        except:
            return {'message': 'An error occurred while creating the delivery.', 'success': 'false'}, 500

        return delivery.json()

    def put(self, order_id):
        delivery = DeliveryModel.find_by_order_id(order_id)

        if delivery:
            if delivery.status == 'Pending':
                data = Delivery.create_parser.parse_args()
                delivery.receiving_address = data['receiving_address']
                delivery.receiver_phone = data['receiver_phone']
                delivery.updated_at = datetime.today()
            else:
                return {'message': 'Can not modify the delivery at this time.', 'success': 'false'}, 400
        else:
            data = Delivery.create_parser.parse_args()

            if data['delivery_unit_id'] or data['delivery_unit_id'] is not None:
                delivery_unit = DeliveryUnitModel.find_by_id(data['delivery_unit_id'])
                if delivery_unit is None:
                    return {'message': 'Delivery unit not found', 'success': 'false'}, 400
            else:
                delivery_unit = DeliveryUnitModel.find_by_id(random.choice(DeliveryUnitModel.get_id_list()))
                data['delivery_unit_id'] = delivery_unit.id

            expected_receving_date = datetime.today() + timedelta(days=delivery_unit.delivery_time)

            delivery = DeliveryModel(order_id, expected_receving_date, datetime.today(), datetime.today(), **data)

        try:
            delivery.save_to_db()
        except:
            return {'message': 'An error occurred while updating the delivery.', 'success': 'false'}, 500

        return delivery.json()

    def delete(self, order_id):
        delivery = DeliveryModel.find_by_order_id(order_id)
        if delivery:
            delivery.delete_from_db()
            return {'message': 'Delivery deleted.', 'success': 'true'}

        return {'message': 'Delivery not found.', 'success': 'false'}, 404


class DeliveryList(Resource):
    def get(self):
        return {'deliveries': list(map(lambda x: x.json(), DeliveryModel.query.all()))}


class DeliveryStatus(Resource):
    def patch(self, order_id):
        delivery = DeliveryModel.find_by_order_id(order_id)

        if delivery:
            data = Delivery.update_parser.parse_args()
            delivery.shipper_id = data['shipper_id']
            delivery.status = data['status']
            delivery.updated_at = datetime.today()
            try:
                delivery.save_to_db()
            except:
                return {'message': 'An error occurred while updating the delivery.', 'success': 'false'}, 500

            return delivery.json()

        return {'message': 'Delivery unit not found', 'success': 'false'}, 404
