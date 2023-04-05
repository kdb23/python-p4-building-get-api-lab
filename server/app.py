#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


# returns an array of JSON objects for all bakeries in the database
@app.route('/bakeries')
def bakeries():
    
    bakeries = []
    for bakery in Bakery.query.all():
        b = bakery.to_dict()
        # bakery_dict = {
        #     "name": bakery.name,
        #     "created_at": bakery.created_at,
        #     "updated_at": bakery.updated_at,
        # } this does not return all the desired information
        bakeries.append(b)

    response = make_response(jsonify(bakeries),200)

    return response

# returns a single bakery as JSON with its baked goods nested in an array. Use the id from the URL to look up the correct bakery.
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(bakery_dict, 200)

    return response

# returns an array of baked goods as JSON, sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = db.session.query(BakedGood).order_by(BakedGood.price.desc()).all()
    baked_goods_json = jsonify([baked_good.to_dict() for baked_good in baked_goods])

    return baked_goods_json

# returns the single most expensive baked good as JSON
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    expensive_json = jsonify(expensive.to_dict())
    return expensive_json

if __name__ == '__main__':
    app.run(port=555, debug=True)
