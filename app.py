print("Starting app.py")
import os
from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS
import stripe

import two_stripe_routes
from thirteen_hook import register_webhook_routes 
from dotenv import load_dotenv
from flask_pymongo import PyMongo


# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')
  

app = Flask(__name__, template_folder='templates', static_folder='react_app/build')
CORS(app)

# Set up MongoDB
app.config["MONGO_URI"] = "mongodb+srv://dcarav77:bambam66@serverlessinstance0.f9h2amf.mongodb.net/Fitness_App"
mongo = PyMongo(app)  # Initialize PyMongo with app

stripe.api_key = os.getenv('STRIPE_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


# Register Stripe routes and webhook routes
two_stripe_routes.register_stripe_routes(app, mongo)
register_webhook_routes(app, mongo)


@app.route('/')
def index():
    return "Welcome to my Flask app!"

@app.route('/api/')
def api_index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
