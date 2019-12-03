from flask_restful import Resource, reqparse

from models.shipper import ShipperModel
from models.delivery_unit import DeliveryUnitModel

class Shipper(Resource):
    create_parser = reqparse.RequestParser()
    create_parser.add_argument('name',
        type = str,
        required = True,
    )
    create_parser.add_argument('phone',
        type = str,
        required = True,
    )
    create_parser.add_argument('delivery_unit_id',
        type = int,
        required = True,
        help = "This field cannot be left blank and must be an integer"
    )

    update_parser = create_parser.copy()
    update_parser.replace_argument('delivery_unit_id',
        type = int,
        help = "This field must be an integer"
    )

    def get(self, shipper_id):
        shipper = ShipperModel.find_by_id(shipper_id)
        if shipper:
            return shipper.json()
        return {'message': 'Shipper not found.'}, 404

    def put(self, shipper_id):
        shipper = ShipperModel.find_by_id(shipper_id)

        if shipper:
            data = Shipper.update_parser.parse_args()

            if data['delivery_unit_id'] or data['delivery_unit_id'] is not None:
                delivery_unit = DeliveryUnitModel.find_by_id(data['delivery_unit_id'])
                if delivery_unit is None:
                    return {'message': 'Delivery unit not found'}, 400

                shipper.delivery_unit_id = data['delivery_unit_id']

            shipper.name = data['name']
            shipper.phone = data['phone']

        else:
            data = Shipper.create_parser.parse_args()
            shipper = ShipperModel(**data)

        try:
            shipper.save_to_db()
        except:
            return {'message': 'An error occurred while updating the shipper.'}, 500

        return shipper.json()

    def delete(self, shipper_id):
        shipper = ShipperModel.find_by_id(shipper_id)
        if shipper:
            shipper.delete_from_db()
            return {'message': 'Shipper deleted.'}

        return {'message': 'Shipper not found.'}, 404


class ShipperList(Resource):
    def get(self):
        return {'shippers': list(map(lambda x: x.json(), ShipperModel.query.all()))}

    def post(self):
        data = Shipper.create_parser.parse_args()

        shipper = ShipperModel(**data)

        try:
            shipper.save_to_db()
        except:
            return {'message': 'An error occurred while creating the shipper.'}, 500

        return shipper.json()
