"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# All the GET Methods
@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route('/people')
def get_all_people():
    people = Character.query.all()
    people = list(map(lambda person: person.serialize(), people))
    return jsonify(people), 200

@app.route('/planet')
def get_all_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/vehicle')
def get_all_vehicles():
    vehicles = Vehicle.query.all()
    vehicles = list(map(lambda vehicle: vehicle.serialize(), vehicles))
    return jsonify(vehicles), 200

@app.route('/favorite')
def get_all_favorites():
    favorites = Favorite.query.all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites), 200

# All the PUT Methods
@app.route('/user', methods=['POST'])
def post_user():
    new_user = User(email="my_super@email.com", first_name="mysupername", last_name="mysuperlastname", password="password1")
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize())

@app.route('/favorite', methods=['POST'])
def change_favorites():
    request_data = request.data
    body = json.loads(request_data)
    if body is None:
        return "This is an Error, body is empty", 400

    if body['user_id'] is None or body['favorite_name'] is None:
        return "Error, either user or favorite doesn't exist", 400

    user = User.query.filter_by(id = body['user_id']).first()
    if user is None:
        return "This is an Error, this user doesn't exist", 400

    favorite = Favorite.query.filter_by(favorite_name = body['favorite_name'], user_id = body['user_id']).first()
    if favorite is not None:
        return "This favorite already exists in the favorites list", 400

    new_favorite = Favorite(favorite_name = body['favorite_name'], user_id = body['user_id'])

    # if body['user_id'] is None and body['planet_id'] is None:
    #     return "This is an Error, missing id", 400

    # user = User.query.filter_by(id = body['user_id']).first()
    # if user is None:
    #     return "This is an Error, this user doesn't exist", 400

    # planet = Planet.query.filter_by(id = body['planet_id']).first()
    # if planet is None:
    #     return "This is an Error, that planet doesn't exist", 400

    # favorite = Favorite.query.filter_by(user_id = body['user_id'], planet_id = body['planet_id']).first()
    # if favorite is not None:
    #     return "Error, favorite already in favorites list", 400

    # new_favorite = Favorite(user_id=body['user_id'], planet_id=body['planet_id'])
    
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize())

# All the DELETE Methods
@app.route('/favorite', methods=['DELETE'])
def delete_favorites():
    request_data = request.data
    body = json.loads(request_data)
    favorite_to_delete = Favorite.query.get(body['favorite_name'])
    if favorite_to_delete is None:
        raise APIException('Error, this item is not in the favorites list', status_code=404)
    db.session.delete(favorite_to_delete)
    db.session.commit()
    return jsonify(favorite_to_delete.serialize())

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
