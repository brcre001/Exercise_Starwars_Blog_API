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
from datetime import datetime
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

@app.route('/favorite')
def get_all_favorites():
    favorites = Favorite.query.all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites), 200

# All the POST Methods
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

@app.route('/user', methods=['POST'])
def create_user():
    request_data = request.get_json()
    new_user = User(first_name=request_data['first_name'], last_name=request_data['last_name'], email=request_data['email'], password=request_data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize())

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
