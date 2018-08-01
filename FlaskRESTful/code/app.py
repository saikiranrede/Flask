from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Sai'
api = Api(app)

jwt = JWT(app, authenticate, identity)   # creates a new endpoint /auth

items = []

class Items(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank'
        )
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)     #using next instead of list cuz, name is identified as unique
        return {'item': item}, 200 if item else 404                       # use list is multiple names match and can return multiple items in a list

    @jwt_required()
    def post(self, name):                                                 #request.get_json(silent=True) processes the request silenty and without rasing error returns None
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': 'The name {} already exists.'.format(name)}, 400
        data = Item.parser.parse_args()                                         #request.get_json(force=True) processes even if header is not mentioned as application/json
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}

api.add_resource(Items, '/item/<string:name>')                            #http://localhost:5000/student/Sai
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
