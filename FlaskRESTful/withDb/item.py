import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Items(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank'
        )
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)    #also can call it as Items.find_by_name
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cur.execute(query, (name,))
        row = result.fetchone()
        conn.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @jwt_required()
    def post(self, name):                                                 #request.get_json(silent=True) processes the request silenty and without rasing error returns None
        if self.find_by_name(name):
            return {'message': 'The name {} already exists.'.format(name)}, 400
        data = Items.parser.parse_args()                                         #request.get_json(force=True) processes even if header is not mentioned as application/json
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {'message': 'An error occurred while inserting an item'}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cur.execute(query, (item['name'], item['price']))
        conn.commit()
        conn.close()

    @jwt_required()
    def delete(self, name):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        query = "DELETE FROM items WHERE name=?"
        cur.execute(query, (name,))
        conn.commit()
        conn.close()
        return {'message': 'item deleted'}

    @jwt_required()
    def put(self, name):
        data = Items.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'An error occurred while inserting an item'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occurred while updating an item'}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cur.execute(query, (item['price'], item['name']))
        conn.commit()
        conn.close()

class ItemList(Resource):
    @jwt_required()
    def get(self):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        query = "SELECT * FROM items"
        result = cur.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        conn.close()
        return {'items': items}
