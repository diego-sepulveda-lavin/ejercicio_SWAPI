"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planet, Vehicle, Favorites_Characters, Favorites_Planets, Favorites_Vehicles
import datetime
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

# GET ALL ROUTES
@app.route('/people', methods=['GET'])
def get_all_people():
    all_characters = Characters.query.all()
    all_characters_serialized = list(map(lambda char: char.serialize2(),all_characters))
    return jsonify(all_characters_serialized), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planet.query.all()
    all_planets_serialized = list(map(lambda planet: planet.serialize2(), all_planets))
    return jsonify(all_planets_serialized), 200

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicle.query.all()
    all_vehicles_serialized = list(map(lambda vehicle: vehicle.serialize2(), all_vehicles))
    return jsonify(all_vehicles_serialized), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    all_users_serialized = list(map(lambda user: user.basic_serialize(), all_users))
    return jsonify(all_users_serialized), 200

#GET BY ID ROUTES
@app.route('/people/<int:uid>', methods=['GET'])
def get_char(uid):
    char = Characters.query.filter_by(uid=uid).first()
    if not char:
        return jsonify({"msg":"Char no encontrado"}), 404
    char = char.serialize()
    return jsonify(char)

@app.route('/planets/<int:uid>', methods=['GET'])
def get_planet(uid):
    planet = Planet.query.filter_by(uid=uid).first()
    if not planet:
        return jsonify({"msg":"Planet no encontrado"}), 404
    planet = planet.serialize()
    return jsonify(planet)

@app.route('/vehicles/<int:uid>', methods=['GET'])
def get_vehicle(uid):
    vehicle = Vehicle.query.filter_by(uid=uid).first()
    if not vehicle:
        return jsonify({"msg":"Vehicle no encontrado"}), 404
    vehicle = vehicle.serialize()
    return jsonify(vehicle)

#POST NEW DATA
@app.route('/people', methods=['POST'])
def create_char():
    name = request.json.get('name')
    height = request.json.get('height')
    mass = request.json.get('mass')
    hair_color = request.json.get('hair_color')
    skin_color = request.json.get('skin_color')
    eye_color = request.json.get('eye_color')
    birth_year = request.json.get('birth_year')
    gender = request.json.get('gender')
    homeworld = request.json.get('homeworld')

    if not name:
        return jsonify({"msg": "El nombre no puede estar vacio"}), 400
    
    new_char = Characters()
    new_char.name = name
    new_char.height = height
    new_char.mass = mass
    new_char.hair_color = hair_color
    new_char.skin_color = skin_color
    new_char.eye_color = eye_color
    new_char.birth_year = birth_year
    new_char.gender = gender
    new_char.homeworld = homeworld

    db.session.add(new_char)
    db.session.commit()

    return jsonify({"msg": "Character creado exitosamente"}), 201

#GET FAV FOR SPECIFIC USER
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg':"User no existe"}), 400
    user = user.serialize()
    return jsonify(user)

#POST NEW FAV
@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def add_favorite(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg":"UserId no valido"}),404

    character_uid = request.json.get('character_uid')
    planet_uid = request.json.get('planet_uid')
    vehicle_uid = request.json.get('vehicle_uid')

    if not character_uid and not planet_uid and not vehicle_uid:
        return jsonify({"msg":"Debes especificar un id de personaje/planet/vehicle"}),400
    
    if character_uid:
        char = Characters.query.get(character_uid)
        if not char:
            return jsonify({"msg":"Id de personaje no valido"}), 404
        
        new_fav = Favorites_Characters()
        new_fav.user_uid = user_id
        new_fav.character_uid = character_uid

        db.session.add(new_fav)
        db.session.commit()
    if planet_uid:
        planet = Planet.query.get(planet_uid)
        if not planet:
            return jsonify({"msg":"Id de planeta no valido"}), 404
        
        new_fav = Favorites_Planets()
        new_fav.user_uid = user_id
        new_fav.planet_uid = planet_uid

        db.session.add(new_fav)
        db.session.commit()
    if vehicle_uid:
        vehicle = Vehicle.query.get(vehicle_uid)
        if not vehicle:
            return jsonify({"msg":"Id de vehicle no valido"}), 404
        
        new_fav = Favorites_Vehicles()
        new_fav.user_uid = user_id
        new_fav.vehicle_uid = vehicle_uid

        db.session.add(new_fav)
        db.session.commit()

    return jsonify({"msg":"Nuevo favorito agregado exitosamente"}),201

#DELETE FAV FOR SPECIFIC USER
@app.route('/users/<int:user_id>/favorites', methods=['DELETE'])
def delete_user_favorite(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg':"User no existe"}), 404
    
    character_uid = request.json.get('character_uid')
    planet_uid = request.json.get('planet_uid')
    vehicle_uid = request.json.get('vehicle_uid')

    if not character_uid and not planet_uid and not vehicle_uid:
        return jsonify({"msg":"Debes especificar un id de personaje/planet/vehicle a eliminar"}),400

    if character_uid:
        char = Favorites_Characters.query.filter_by(user_uid=user_id,character_uid=character_uid).first()
        if not char:
            return jsonify({"msg":"Id de personaje no valido"}), 404

        db.session.delete(char)
        db.session.commit()
    if planet_uid:
        planet = Favorites_Planets.query.filter_by(user_uid=user_id,planet_uid=planet_uid).first()
        if not planet:
            return jsonify({"msg":"Id de planeta no valido"}), 404
        
        db.session.delete(planet)
        db.session.commit()
    if vehicle_uid:
        vehicle = Favorites_Vehicles.query.filter_by(user_uid=user_id,vehicle_uid=vehicle_uid).first()
        if not vehicle:
            return jsonify({"msg":"Id de vehicle no valido"}), 404
        
        db.session.delete(vehicle)
        db.session.commit()

    return jsonify({"msg":"Favorito eliminado exitosamente"}),201

#DELETE PEOPLE, PLANET, VEHICLE BY ID
@app.route('/people/<int:delete_id>', methods=['DELETE'])
def delete_char_by_id(delete_id):
    char_to_delete = Characters.query.get(delete_id)
    if not char_to_delete:
        return jsonify({"msg":"Char id incorrecto"})
    
    db.session.delete(char_to_delete)
    db.session.commit()

    return jsonify({"msg":"Char eliminado exitosamente"}),201

@app.route('/planets/<int:delete_id>', methods=['DELETE'])
def delete_planet_by_id(delete_id):
    planet_to_delete = Planet.query.get(delete_id)
    if not planet_to_delete:
        return jsonify({"msg":"Planet id incorrecto"})
    
    db.session.delete(planet_to_delete)
    db.session.commit()

    return jsonify({"msg":"Planet eliminado exitosamente"}),201

@app.route('/vehicles/<int:delete_id>', methods=['DELETE'])
def delete_vehicle_by_id(delete_id):
    vehicle_to_delete = Vehicle.query.get(delete_id)
    if not vehicle_to_delete:
        return jsonify({"msg":"Vehicle id incorrecto"})
    
    db.session.delete(vehicle_to_delete)
    db.session.commit()

    return jsonify({"msg":"Vehicle eliminado exitosamente"}),201

#DELETE USER BY ID
@app.route('/user/<int:delete_id>', methods=['DELETE'])
def delete_user_by_id(delete_id):
    user_to_delete = User.query.get(delete_id)
    if not user_to_delete:
        return jsonify({"msg":"User id incorrecto"})
    
    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({"msg":"User eliminado exitosamente"}),201

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
