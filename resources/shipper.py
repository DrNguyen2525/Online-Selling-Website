from flask_restful import Resource
from models.shipper import ShipperModel

class Shipper(Resource):
    def get(self, order_id):
        shipper = ShipperModel.find_by_order_id(order_id)
        if shipper:
            return shipper.json()
        return {'message': 'Shipper not found'}, 404

    def post(self, order_id):
        if ShipperModel.find_by_order_id(order_id):
            return {'message': "A shipper with order_id '{}' already exists.".format(order_id)}, 400

        shipper = ShipperModel(order_id)
        try:
            shipper.save_to_db()
        except:
            return {'message': 'An error occurred while creating the shipper.'}, 500

        return shipper.json()

    # def put(self, order_id):
    #     data = Shipper.parser.parse_args()
    #
    #     shipper = ShipperModel.find_by_order_id(order_id)
    #
    #     if shipper is None:
    #         shipper = ShipperModel(order_id, **data)
    #     else:
    #         shipper.price = data['price']
    #
    #     shipper.save_to_db()
    #
    #     return shipper.json()

    def delete(self, order_id):
        shipper = ShipperModel.find_by_order_id(order_id)
        if shipper:
            shipper.delete_from_db()

        return {'message': 'Shipper deleted.'}


class ShipperList(Resource):
    def get(self):
        return {'shippers': list(map(lambda x: x.json(), ShipperModel.query.all()))}
