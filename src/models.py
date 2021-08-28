import os, datetime
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Users(db.Model)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    favorite_character = db.relationship('FavoriteCharacter', back_populates="user")
    favorite_planet = db.relationship('FavoritePlanet', back_populates="user")
    favorite_vehicle = db.relationship('FavoriteVehicle', back_populates="user")

    def __repr__(self):
        return self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
            "join_date": self.join_date
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(80), nullable=True)
    skin_color = db.Column(db.String(80), nullable=True)
    eye_color = db.Column(db.String(80), nullable=True)
    birth_year = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=True)
    edited = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    users = db.relationship("FavoriteCharacter", back_populates="character")

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "edited": self.edited,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    edited = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    users = db.relationship("FavoritePlanet", back_populates="planet")

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "edited": self.edited
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    users = db.relationship("FavoriteVehicle", back_populates="vehicle")

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "cargo_capacity": self.cargo_capacity,
            "created": self.created
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite-character'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    character_id = db.Column(db.ForeignKey('character.id'))
    character = db.relationship("Character", back_populates="users")
    user = db.relationship("User", back_populates="favorite_character")

    def __repr__(self):
        return '<Favorite Character%r>' % self.character

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite-planet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    planet_id = db.Column(db.ForeignKey('planet.id'))
    planet = db.relationship("Planet", back_populates="users")
    user = db.relationship("User", back_populates="favorite_planet")

    def __repr__(self):
        return '<Favorite Planet%r>' % self.planet

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

class FavoriteVehicle(db.Model):
    __tablename__ = 'favorite-vehicle'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.ForeignKey('vehicle.id'))
    vehicle = db.relationship("Vehicle", back_populates="users")
    user = db.relationship("User", back_populates="favorite_vehicle")

    def __repr__(self):
        return '<Favorite Vehicle%r>' % self.vehicle

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id
        }