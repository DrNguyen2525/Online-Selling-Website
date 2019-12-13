from flask_restful import Resource, reqparse

from models.delivery_unit import DeliveryUnitModel

class DeliveryUnit(Resource):
    create_parser = reqparse.RequestParser()
    create_parser.add_argument('name',
        type = str,
        required = True,
    )
    create_parser.add_argument('base_fee',
        type = float,
        required = True,
        help = "This field cannot be left blank and must be a float number"
    )
    create_parser.add_argument('delivery_time',
        type = int,
        required = True,
        help = "This field cannot be left blank and must be an integer"
    )

    update_parser = create_parser.copy()

    def get(self, delivery_unit_id):
        delivery_unit = DeliveryUnitModel.find_by_id(delivery_unit_id)
        if delivery_unit:
            return delivery_unit.json()
        return {'message': 'Delivery unit not found'}, 404

    def put(self, delivery_unit_id):
        delivery_unit = DeliveryUnitModel.find_by_id(delivery_unit_id)

        if delivery_unit:
            data = DeliveryUnit.update_parser.parse_args()
            delivery_unit.name = data['name']
            delivery_unit.base_fee = data['base_fee']
            delivery_unit.delivery_time = data['delivery_time']
        else:
            data = DeliveryUnit.create_parser.parse_args()

            if DeliveryUnitModel.find_by_name(data['name']):
                return {'message': f'A delivery unit with name {data['name']} already exists.'}, 400

            delivery_unit = DeliveryUnitModel(**data)

        try:
            delivery_unit.save_to_db()
        except:
            return {'message': 'An error occurred while updating the delivery unit.'}, 500

        return delivery_unit.json()

    def delete(self, delivery_unit_id):
        delivery_unit = DeliveryUnitModel.find_by_id(delivery_unit_id)
        if delivery_unit:
            delivery_unit.delete_from_db()
            return {'message': 'Delivery unit deleted.'}

        return {'message': 'Delivery unit not found.'}, 404


class DeliveryUnitList(Resource):
    def get(self):
        return {'delivery_units': list(map(lambda x: x.json(), DeliveryUnitModel.query.all()))}

    def post(self):
        data = DeliveryUnit.create_parser.parse_args()

        if DeliveryUnitModel.find_by_name(data['name']):
            return {'message': "A delivery unit with name '{}' already exists.".format(data['name'])}, 400

        delivery_unit = DeliveryUnitModel(**data)

        try:
            delivery_unit.save_to_db()
        except:
            return {'message': 'An error occurred while creating the delivery unit.'}, 500

        return delivery_unit.json()
