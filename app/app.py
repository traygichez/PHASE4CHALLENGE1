#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from flask_cors import CORS, cross_origin

from models import db, Hero, Power, HeroPower

import os

abs_path = os.getcwd()
abs_python_path = os.path.normpath(abs_path)


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{abs_path}/db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Index(Resource):  
    @cross_origin
    def get(self):
        response_dict = {
            "index": "Welcome to the Heros RESTful API",
        }
        return jsonify(response_dict) 
    
 
api.add_resource(Index, '/')


class Heroes(Resource):

    def get(self):
        heroes = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in Hero.query.all()]
        return make_response(jsonify(heroes), 200)

api.add_resource(Heroes, '/heroes')

class OneHero(Resource):

    def get(self, id):

            hero = Hero.query.filter_by(id=id).first()
            
            if hero:
                hero_data = {
                    "id": hero.id,
                    "name": hero.name,
                    "super_name": hero.super_name,
                    "powers": [
                        {
                            "id": hero_power.power.id,
                            "name": hero_power.power.name,
                            "description": hero_power.power.description
                        }
                        for hero_power in hero.hero_powers
                    ]
                }

                return hero_data

            return {
                "error": "Hero not found"
            }, 404        

api.add_resource(OneHero, '/heroes/<int:id>')

class Powers(Resource):

    def get(self):
        powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in Power.query.all()]
        return make_response(jsonify(powers), 200)

api.add_resource(Powers, '/powers')

class OnePower(Resource):

    def get(self, id):

            power = Power.query.filter_by(id=id).first()
            
            if power:
                power_data = {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description,
                }

                return power_data

            return {
                "error": "Power not found"
            }, 404 
      
    def patch(self, id):

        power = Power.query.filter(Power.id == id).first()

        data = request.get_json()

        if power:
            for attr in data:
                setattr(power, attr, data[attr])

            db.session.add(power)
            db.session.commit()

            response_body = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }

            return response_body, 201

        return {
            "error": "Power not found"
        }, 400

         

api.add_resource(OnePower, '/powers/<int:id>')

class HeroPowers(Resource):

    def post(self):

        data = request.get_json()

        hero = Hero.query.filter(Hero.id == data['hero_id']).first()
        power = Power.query.filter(Power.id == data['power_id']).first()

        if not hero or not power:
            return {
                "errors": ["Hero or Power doesn't exist"]
            }, 404

        new_hero_power = HeroPower(
            strength=data['strength'],
            power_id=data['power_id'],
            hero_id=data['hero_id']
        )

        db.session.add(new_hero_power)
        db.session.commit()

        hero_data = OneHero().get(hero.id)

        return hero_data, 201


api.add_resource(HeroPowers, '/hero_powers')




if __name__ == '__main__':
    app.run(port=5555)
