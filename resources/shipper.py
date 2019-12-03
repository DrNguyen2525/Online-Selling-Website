from flask_restful import Resource, reqparse

from models.shipper import ShipperModel

class Shipper(Resource):
    create_parser = reqparse.RequestParser()
    create_parser.add_argument('name',
        type = str,
        required = True,
        help = "The field 'name' cannot be left blank."
    )
    create_parser.add_argument('phone',
        type = str,
        required = True,
        help = "The field 'phone' cannot be left blank."
    )

    update_parser = reqparse.RequestParser()
    update_parser.add_argument('name',
        type = str,
        required = True,
        help = "The field 'name' cannot be left blank."
    )
    update_parser.add_argument('phone',
        type = str,
        required = True,
        help = "The field 'phone' cannot be left blank."
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
