from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    first_name = db.Column(db.String(20)) 
    second_name = db.Column(db.String(20))
    fav_characters = db.relationship("Favorites_Characters", cascade="all, delete")
    fav_planets = db.relationship("Favorites_Planets", cascade="all, delete")
    fav_vehicles = db.relationship("Favorites_Vehicles", cascade="all, delete")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.uid,
            "email": self.email,
            "fav_characters": list(map(lambda fav_char: fav_char.serialize(),self.fav_characters)),
            "fav_planets": list(map(lambda fav_planet: fav_planet.serialize(),self.fav_planets)),
            "fav_vehicles": list(map(lambda fav_vehicle: fav_vehicle.serialize(), self.fav_vehicles))
        }
    
    def basic_serialize(self):
        return {
            "id": self.uid,
            "email": self.email,
            "is_active": self.is_active
        }


class Characters(db.Model):
    __tablename__ = "characters"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20)) 
    height = db.Column(db.Float)
    mass = db.Column(db.Float)
    hair_color = db.Column(db.String(20)) 
    skin_color = db.Column(db.String(20)) 
    eye_color = db.Column(db.String(20)) 
    birth_year = db.Column(db.Date) 
    gender = db.Column(db.String(20)) 
    created = db.Column(db.Date, default=datetime.datetime.now()) 
    edited = db.Column(db.Date, default=datetime.datetime.now()) 
    homeworld = db.Column(db.String(20))
    like_by_users = db.relationship("Favorites_Characters", backref="character", cascade="all, delete")

    def __repr__(self):
        return '<Character %r, %r>' % (self.uid, self.name)
        

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "height" : self.height,
            "mass" : self.mass,
            "hair_color" : self.hair_color,
            "skin_color" : self.skin_color,
            "eye_color" : self.eye_color,
            "birth_year" : self.birth_year,
            "gender" : self.gender,
            "created" : self.created,
            "edited" : self.edited,
            "homeworld" : self.homeworld,
        }
        
    def serialize2(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "url": f"https://3000-sapphire-felidae-jkwjegdk.ws-us03.gitpod.io/people/{self.uid}"
        }

class Planet(db.Model):
    __tablename__ = "planet"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20)) 
    diameter = db.Column(db.Float)
    rotation_period = db.Column(db.Float)
    orbital_period = db.Column(db.Float)
    gravity = db.Column(db.Float)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(20)) 
    terrain = db.Column(db.String(20)) 
    surface_water = db.Column(db.Integer)
    created = db.Column(db.Date, default=datetime.datetime.now())
    edited = db.Column(db.Date)
    like_by_users = db.relationship("Favorites_Planets", backref="planet",cascade="all, delete")

    def __repr__(self):
        return '<Planet %r, %r>' % (self.uid, self.name)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "diameter" : self.diameter,
            "rotation_period" : self.rotation_period,
            "orbital_period" : self.orbital_period,
            "gravity" : self.gravity,
            "population" : self.population,
            "climate" : self.climate,
            "terrain" : self.terrain,
            "surface_water" : self.surface_water,
            "created" : self.created,
            "edited" : self.edited,
        }
    
    def serialize2(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "url": f"https://3000-sapphire-felidae-jkwjegdk.ws-us03.gitpod.io/planets/{self.uid}"
        }

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20)) 
    model = db.Column(db.String(20)) 
    starship_class = db.Column(db.String(20)) 
    manufacturer = db.Column(db.String(20)) 
    cost_in_credits = db.Column(db.Integer) 
    length = db.Column(db.Float) 
    crew = db.Column(db.Float) 
    passengers = db.Column(db.Integer) 
    max_atmosphering_speed = db.Column(db.Float) 
    hyperdrive_rating = db.Column(db.Float) 
    mglt = db.Column(db.Integer) 
    cargo_capacity = db.Column(db.Integer) 
    consumables = db.Column(db.String(20)) 
    pilots = db.Column(db.Integer) 
    created = db.Column(db.Date, default=datetime.datetime.now())
    edited = db.Column(db.Date)
    like_by_users = db.relationship("Favorites_Vehicles", backref="vehicle", cascade="all, delete")

    def __repr__(self):
        return '<Vehicle %r, %r>' % (self.uid, self.name)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "model" : self.model,
            "starship_class" : self.starship_class,
            "manufacturer" : self.manufacturer,
            "cost_in_credits" : self.cost_in_credits,
            "length" : self.length,
            "crew" : self.crew,
            "passengers" : self.passengers,
            "max_atmosphering_speed" : self.max_atmosphering_speed,
            "hyperdrive_rating" : self.hyperdrive_rating,
            "mglt" : self.mglt,
            "cargo_capacity" : self.cargo_capacity,
            "consumables" : self.consumables,
            "pilots" : self.pilots,
            "created" : self.created,
            "edited" : self.edited,
        }

    def serialize2(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "url": f"https://3000-sapphire-felidae-jkwjegdk.ws-us03.gitpod.io/vehicles/{self.uid}"
        }

class Favorites_Characters(db.Model):
    __tablename__ = "favorites_characters"
    uid = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    character_uid = db.Column(db.Integer, db.ForeignKey('characters.uid'))

    def serialize(self):
        return self.character.serialize2()
    

class Favorites_Vehicles(db.Model):
    __tablename__ = "favorites_vehicles"
    uid = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    vehicle_uid = db.Column(db.Integer, db.ForeignKey('vehicle.uid'))

    def serialize(self):
        return self.vehicle.serialize2()

class Favorites_Planets(db.Model):
    __tablename__ = "favorites_planets"
    uid = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    planet_uid = db.Column(db.Integer, db.ForeignKey('planet.uid'))

    def serialize(self):
        return self.planet.serialize2()