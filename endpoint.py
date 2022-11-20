from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonpify

db_connect = create_engine('sqlite:///users.db')
app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from users")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class User(Resource):
    def get(self, user_id):
        conn = db_connect.connect()
        query = conn.execute("select * from users where id =%d "  %int(user_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class CreateUser(Resource):
    def post(self):
        conn = db_connect.connect()
        query = conn.execute("select * from users where email = '%s'" %request.json['email'])
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if len(result['data']) > 0:
            return {'status':'user already exists'}
        else:
            if request.json['first_name'] and request.json['last_name'] and request.json['email'] and request.json['age'] and request.json['country'] and request.json['genre'] and request.json['birthday'] and request.json['phone']:
                first_name = request.json['first_name']
                last_name = request.json['last_name']
                email = request.json['email']
                age = request.json['age']
                country = request.json['country']
                genre = request.json['genre']
                birthday = request.json['birthday']
                phone = request.json['phone']
                query = conn.execute("insert into users values(null, '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(first_name, last_name, email, age, country, genre, birthday, phone))
                return {'status':'success'}
            else:
                return {'status':'error'}

class UpdateUser(Resource):
    def put(self, user_id):
        conn = db_connect.connect()
        query = conn.execute("select * from users where id =%d "  %int(user_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'error', 'message':'user not found'}
        if request.json['first_name'] and request.json['last_name'] and request.json['email'] and request.json['age'] and request.json['country'] and request.json['genre'] and request.json['birthday'] and request.json['phone']:
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            email = request.json['email']
            age = request.json['age']
            country = request.json['country']
            genre = request.json['genre']
            birthday = request.json['birthday']
            phone = request.json['phone']
            query = conn.execute("update users set first_name = '{0}', last_name = '{1}', email = '{2}', age = '{3}', country = '{4}', genre = '{5}', birthday = '{6}', phone = '{7}' where id = {8}".format(first_name, last_name, email, age, country, genre, birthday, phone, user_id))
            return {'status':'success'}
        else:
            return {'status':'error', 'message':'missing fields'}

class DeleteUser(Resource):
    def delete(self, user_id):
        conn = db_connect.connect()
        #validar si el usuario existe
        query = conn.execute("select * from users where id =%d "  %int(user_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'error', 'message':'user not found'}
        else:
            conn.execute("delete from users where id =%d "  %int(user_id))
            return {'status':'success'}

@app.route('/')
def index():
    return "Hello, World!"

@app.errorhandler(404)
def page_not_found(e):
    return "Ups, 404"

api.add_resource(Users, '/users') # Route_1
api.add_resource(User, '/users/<user_id>') # Route_2
api.add_resource(CreateUser, '/users') # Route_3
api.add_resource(UpdateUser, '/users/<user_id>') # Route_4
api.add_resource(DeleteUser, '/users/<user_id>') # Route_5

if __name__ == '__main__':
    app.run(port='5002')
