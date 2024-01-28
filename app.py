import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import stripe
from flask_pymongo import PyMongo
import two_stripe_routes
from thirteen_hook import register_webhook_routes
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

app = Flask(__name__, template_folder='templates', static_folder='react_app/build')
CORS(app)

# MongoDB setup
app.config["MONGO_URI"] = "mongodb+srv://dcarav77:bambam66@serverlessinstance0.f9h2amf.mongodb.net/Fitness_App"
mongo = PyMongo(app)

# Stripe setup
stripe.api_key = os.getenv('STRIPE_API_KEY')

# Register routes
two_stripe_routes.register_stripe_routes(app, mongo)
register_webhook_routes(app, mongo)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/')
def api_index():
    return jsonify({'message': 'API is working'})

if __name__ == '__main__':
    app.run(debug=True)
