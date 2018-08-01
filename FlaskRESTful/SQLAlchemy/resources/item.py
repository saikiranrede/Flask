from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Items(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank'
        )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = 'Every item needs a store_id'
        )
        
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)    #also can call it as Items.find_by_name
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'The name {} already exists.'.format(name)}, 400
        data = Items.parser.parse_args()
        item = ItemModel(name, **data)                    #can also use data['price'], data['store_id']
        try:
            item.upsert()
        except:
            return {'message': 'An error occurred while inserting an item'}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Items.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)               #can also use data['price'], data['store_id']
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.upsert()
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}   #also can use lambda list(map(lambda x: x.json(), ItemModel.query.all()))
