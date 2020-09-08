# Section 4, Videos 71 onwards I think
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # Creates new endpoint, known as / auth

items = []


# Note that in the code below, we do not specifically need to specify jsonify
# This is because flask_restful does that for us.

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()  # By using the decorator at a specific method, it would then require authorization
    # Instead of doing a for loop, you can do something called filter.
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        # This just gets the one we want (look at lamba lecture), if multiple,
        # say list(filter "and what ever condition)

        # for item in items:
        # if item['name'] == name:
        # return item
        return {'item': item}, 200 if item else 404

    # 404 is the status code for an item not being found.
    # Keep in mind that the most popular status code is 200, it is a popular
    # interview question.

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400  # Means bad request
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # 201 means created

    # 201 means some data has been found and returned.
    # 202 also means accepted, but you are delaying the creation.

    # For example, if an object takes a long time to be created, then you
    # would say 202.

    def delete(self, name):
        global items  # Refers to the global variable items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'Item deleted'}
    
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
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# In the line above, instead of doing the decorator like saying @app.route,
# you just do the string format instead.

app.run(port=5000, debug=True)



