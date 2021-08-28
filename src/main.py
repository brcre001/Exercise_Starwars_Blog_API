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
from models import db, User, Character, Planet, Vehicle, FavoriteCharacter, FavoritePlanet, FavoriteVehicle
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "secret_key"  # Change this "super secret" with something else!
jwt = JWTManager(app)
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

@app.route('/user/<int:id>')
def get_specific_user(id):
    user = User.query.filter_by(id=id)
    user = user.serialize()
    return jsonify(user), 200

@app.route('/people')
def get_all_people():
    people = Character.query.all()
    people = list(map(lambda person: person.serialize(), people))
    return jsonify(people), 200

@app.route('/people/<int:id>')
def get_a_person(id):
    person = Character.query.get(id)
    person = person.serialize()
    return jsonify(person), 200

@app.route('/planet')
def get_all_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/planet/<int:id>')
def get_a_planet(id):
    planet = Planet.query.get(id)
    planet = planet.serialize()
    return jsonify(planet), 200

@app.route('/vehicle')
def get_all_vehicles():
    vehicles = Vehicle.query.all()
    vehicles = list(map(lambda vehicle: vehicle.serialize(), vehicles))
    return jsonify(vehicles), 200

@app.route('/vehicle/<int:id>')
def get_a_vehicle(id):
    vehicle = Vehicle.query.get(id)
    vehicle = vehicle.serialize()
    return jsonify(vehicle), 200

# @app.route('/favorite/people/')
# def get_favorite_characters(id):
#     vehicle = Vehicle.query.get(id)
#     vehicle = vehicle.serialize()
#     return jsonify(vehicle), 200

# @app.route('/user/favorite/people', methods=['GET'])
# def user_favorite():
#     favorite_query = FavoriteCharacter.query.filter_by(user_id = 1)
#     map_favorite = [item.serialize() for item in favorite_query]
#     return jsonify(map_favorite)

# ALL THE POST METHODS

@app.route('/user', methods=['POST'])
def create_user():
    request_data = request.get_json()
    new_user = User(first_name=request_data['first_name'], last_name=request_data['last_name'], email=request_data['email'], password=request_data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize())

@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad email or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

# POST methods for creating new STARWARS items

@app.route('/people', methods=['POST'])
def create_character():
    request_data = request.get_json()
    if 'name' in request_data:
        character = Character(name=request_data['name'], hair_color=request_data['hair_color'], skin_color=request_data['skin_color'], eye_color=request_data['eye_color'], birth_year=request_data['birth_year'], gender=request_data['gender'])
    else:
        return "This is a wrong request", 400
    db.session.add(character)
    db.session.commit()
    return jsonify(character.serialize())

@app.route('/planet', methods=['POST'])
def create_planet():
    request_data = request.get_json()
    if 'orbital_period' in request_data:
        planet = Planet(name=request_data['name'], orbital_period=request_data['orbital_period'], gravity=request_data['gravity'], population=request_data['population'], climate=request_data['climate'])
    else:
        return "This is a wrong request", 400
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize())

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    request_data = request.get_json()
    if 'model' in request_data:
        vehicle = Vehicle(name=request_data['name'], model=request_data['model'], manufacturer=request_data['manufacturer'], cost_in_credits=request_data['cost_in_credits'], length=request_data['length'], cargo_capacity=request_data['cargo_capacity'])
    else:
        return "This is a wrong request", 400
    db.session.add(vehicle)
    db.session.commit()
    return jsonify(vehicle.serialize())

# POST Methods for Creating Favorites

@app.route('/user/<int:user_id>/favorite/people/<int:character_id>', methods=["POST"])
def add_fav(user_id, character_id):
    fav = FavoriteCharacter(
        user_id = user_id,
        character_id = character_id
    )
    character = FavoriteCharacter.query.filter_by(character_id=character_id, user_id=user_id).first()
    character = character.serialize()
    if character['character_id'] == character_id and character['user_id'] == user_id:
        return "This favorite character already exists for this user", 400
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize())

@app.route('/user/<user_id>/favorite/people')
def get_favorite_character(user_id):
    fav = FavoriteCharacter.query.get(user_id)
    fav = list(map(lambda person: person.serialize(), fav))
    return jsonify(fav), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
