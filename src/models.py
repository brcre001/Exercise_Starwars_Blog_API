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
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String(250), nullable=False)
    last_name = db.Column(String(250), nullable=False)
    email = db.Column(String(250), nullable=False)
    password = db.Column(String(80), nullable=False)
    join_date = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    favorite = db.relationship('Favorite')

    def __repr__(self):
        return '<Users %r>' % self.first_name

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
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    height = db.Column(String(80), nullable=False)
    mass = db.Column(String(80), nullable=False)
    hair_color = db.Column(String(80), nullable=True)
    skin_color = db.Column(String(80), nullable=True)
    eye_color = db.Column(String(80), nullable=True)
    birth_year = db.Column(String(250), nullable=False)
    gender = db.Column(String(250), nullable=True)
    created = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    edited = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    homeworld = db.Column(String(250), nullable=False)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "created": self.created,
            "edited": self.edited,
            "homeworld": self.homeworld
        }

class Planet(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    diameter = db.Column(Integer, nullable=False)
    rotation_period = db.Column(Integer, nullable=False)
    orbital_period = db.Column(Integer, nullable=False)
    gravity = db.Column(String(250), nullable=False)
    population = db.Column(Integer, nullable=False)
    climate = db.Column(String(250), nullable=False)
    terrain = db.Column(String(250), nullable=False)
    surface_water = db.Column(String(250), nullable=False)
    created = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    edited = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created,
            "edited": self.edited
        }

class Vehicle(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    model = db.Column(String(250), nullable=False)
    starship_class = db.Column(String(250), nullable=False)
    manufacturer = db.Column(String(250), nullable=False)
    cost_in_credits = db.Column(Integer, nullable=False)
    length = db.Column(Integer, nullable=False)
    crew = db.Column(Integer, nullable=False)
    passengers = db.Column(Integer, nullable=False)
    max_atmosphering_speed = db.Column(Integer, nullable=False)
    hyperdrive_rating = db.Column(String(250), nullable=False)
    MGLT = db.Column(Integer, nullable=False)
    cargo_capacity = db.Column(Integer, nullable=False)
    consumables = db.Column(String(250), nullable=False)
    pilots = db.Column(String(250), nullable=False)
    created = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    edited = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "startship_class": self.starship_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "pilots": self.pilots,
            "created": self.created,
            "edited": self.edited
        }

class Favorite(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(ForeignKey('user.id'))
    favorite_name = db.Column(String(250), nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.favorite_name

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_name": self.favorite_name
        }

## Draw from SQLAlchemy base
# render_er(Base, 'diagram.png')