import os
from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS
import stripe
import two_stripe_routes
from five_hook import register_webhook_routes 
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

app = Flask(__name__, template_folder='templates', static_folder='react_app/build')
CORS(app)

# Stripe and SendGrid configuration
#stripe.api_key = os.getenv('STRIPE_API_KEY')
stripe.api_key = 'sk_test_51O7mnXEBiprZstxkH0Lhrcv9OGoe1ZiSOHANZvv8L8kICroOFyzVidtNYAau6C3LFtdZAtNy1xStifVvIyKPYAlS00fsbC5wi7'
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


# Register Stripe routes and webhook routes
two_stripe_routes.register_stripe_routes(app)
register_webhook_routes(app)


@app.route('/')
def index():
    return "Welcome to my Flask app!"

@app.route('/api/')
def api_index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
