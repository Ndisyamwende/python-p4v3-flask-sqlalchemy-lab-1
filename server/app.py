# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from flask import Flask, jsonify, make_response


from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    # Query the database to get the earthquake with the specified ID
    earthquake = Earthquake.query.get(id)

    # Check if earthquake exists
    if earthquake:
        # Return JSON response with earthquake attributes
        return jsonify({
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }), 200
    else:
        # Return error message if no earthquake is found
        return jsonify({'error': 'Earthquake not found'}), 404
    
@app.route('/earthquakes/magnitude/<float:min_magnitude>')
def get_earthquakes_by_magnitude(min_magnitude):
    # Query the database to get earthquakes with magnitude greater than or equal to the specified value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= min_magnitude).all()

    # Count the number of matching earthquakes
    count = len(earthquakes)

    # Create a list containing data for each matching earthquake
    quakes_data = [{
        'id': quake.id,
        'location': quake.location,
        'magnitude': quake.magnitude,
        'year': quake.year
    } for quake in earthquakes]

    # Return JSON response with count and earthquake data
    return jsonify({'count': count, 'quakes': quakes_data}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
