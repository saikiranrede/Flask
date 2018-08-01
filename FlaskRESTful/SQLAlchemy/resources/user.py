from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'username cannot be left blank'
        )
    parser.add_argument('password',
        type = str,
        required = True,
        help = 'password cannot be left blank'
        )

    @jwt_required()
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'The username already exists'}, 400
        user = UserModel(**data)                    # can also use (data['username'], data['password'])
        user.upsert()
        return {'message': 'User created successfully'}, 201
