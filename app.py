"""Flask app for Cupcakes"""
import os
from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get('/api/cupcakes')
def show_all_cupcake_data():
    '''returns all cupcake data in JSON format

    example data:
    {cupcakes: [{id, flavor, size, rating, image_url}, ...]}
    '''

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>') #QUESTION: why no int?
def get_cupcake_id(cupcake_id):
    '''returns data about a single cupcake'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def add_cupcake():
    '''returns new cupcake data in JSON format

    returns JSON:
    {cupcake: [{id, flavor, size, rating, image_url}, ...]}
    '''

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image_url']

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image_url=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def edit_cupcake(cupcake_id):
    '''Respond with JSON of the newly-updated cupcake

      Like this: {cupcake: {id, flavor, size, rating, image_url}}.'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image_url = request.json.get('image_url', cupcake.image_url)


    db.session.commit()
    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.delete('/api/cupcakes/<int:cupcake_id>')
def deletes_cupcake(cupcake_id):
    """deletes cupcake or return 404 if the cupcake cannot be found


    respond with JSON like: {deleted: [cupcake-id]}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)


    db.session.delete(cupcake)

    db.session.commit()

    response = {'deleted': [cupcake_id]}
    print(response)


    return jsonify(response)
