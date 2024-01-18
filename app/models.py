from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    hero_powers = db.relationship('HeroPower', backref='hero')

    def __repr__(self):
        return f'<Hero {self.name}>'


# add any models you may need. 
class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    hero_powers = db.relationship('HeroPower', backref='power')

    @validates('description')
    def validate_description(self, key, value):
        if not value:
            raise ValueError("Description must be present")
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value


    def __repr__(self):
        return f'<Power {self.name}>'


class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable = False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable = False)

    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError("Invalid strength value")
        return value

    def __repr__(self):
        return f'<HeroPower {self.strength}>'