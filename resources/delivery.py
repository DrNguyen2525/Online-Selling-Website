from flask_restful import Resource, reqparse
from datetime import datetime

from models.delivery import DeliveryModel

class Delivery(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('receiving_address',
        type = str,
        required = True,
        help = "The field 'receiving_address' cannot be left blank."
    )
    parser.add_argument('receiver_phone',
        type = str,
        required = True,
        help = "The field 'receiver_phone' cannot be left blank."
    )
    parser.add_argument('total_cost',
        type = int,
        required = True,
        help = "The field 'total_cost' cannot be left blank.."
    )

    def get(self, order_id):
        delivery = DeliveryModel.find_by_order_id(order_id)
        if delivery:
            return delivery.json()
        return {'message': 'Delivery not found'}, 404

    def post(self, order_id):
        if DeliveryModel.find_by_order_id(order_id):
            return {'message': "A delivery with order_id '{}' already exists.".format(order_id)}, 400

        data = Delivery.parser.parse_args()

        delivery = DeliveryModel(order_id, datetime.today(), **data)

        try:
            delivery.save_to_db()
        except:
            return {'message': 'An error occurred while creating the delivery.'}, 500

        return delivery.json()

    # def put(self, order_id):
    #     data = Delivery.parser.parse_args()
    #
    #     delivery = DeliveryModel.find_by_order_id(order_id)
    #
    #     if delivery is None:
    #         delivery = DeliveryModel(order_id, **data)
    #     else:
    #         delivery.price = data['price']
    #
    #     delivery.save_to_db()
    #
    #     return delivery.json()

    def delete(self, order_id):
        delivery = DeliveryModel.find_by_order_id(order_id)
        if delivery:
            delivery.delete_from_db()
            return {'message': 'Delivery deleted.'}

        return {'message': 'Delivery not found'}, 404


class DeliveryList(Resource):
    def get(self):
        return {'deliveries': list(map(lambda x: x.json(), DeliveryModel.query.all()))}
