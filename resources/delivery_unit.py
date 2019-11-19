from flask_restful import Resource
from models.delivery_unit import DeliveryUnitModel

class DeliveryUnit(Resource):
    def get(self, order_id):
        delivery_unit = DeliveryUnitModel.find_by_order_id(order_id)
        if delivery_unit:
            return delivery_unit.json()
        return {'message': 'DeliveryUnit not found'}, 404

    def post(self, order_id):
        if DeliveryUnitModel.find_by_order_id(order_id):
            return {'message': "A delivery_unit with order_id '{}' already exists.".format(order_id)}, 400

        delivery_unit = DeliveryUnitModel(order_id)
        try:
            delivery_unit.save_to_db()
        except:
            return {'message': 'An error occurred while creating the delivery_unit.'}, 500

        return delivery_unit.json()

    # def put(self, order_id):
    #     data = DeliveryUnit.parser.parse_args()
    #
    #     delivery_unit = DeliveryUnitModel.find_by_order_id(order_id)
    #
    #     if delivery_unit is None:
    #         delivery_unit = DeliveryUnitModel(order_id, **data)
    #     else:
    #         delivery_unit.price = data['price']
    #
    #     delivery_unit.save_to_db()
    #
    #     return delivery_unit.json()

    def delete(self, order_id):
        delivery_unit = DeliveryUnitModel.find_by_order_id(order_id)
        if delivery_unit:
            delivery_unit.delete_from_db()

        return {'message': 'DeliveryUnit deleted.'}


class DeliveryUnitList(Resource):
    def get(self):
        return {'delivery_units': list(map(lambda x: x.json(), DeliveryUnitModel.query.all()))}
