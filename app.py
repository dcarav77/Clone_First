from flask import Flask, render_template, send_from_directory, jsonify
#import stripe_routes
from flask_cors import CORS
import two_stripe_routes

app = Flask(__name__, template_folder='templates', static_folder='react_app/build')

CORS(app)

# Register Stripe routes
two_stripe_routes.register_stripe_routes(app)

@app.route('/webhook', methods=['POST']) #added this webhook for stripe
def webhook():
    print("Webhook from script 1 triggered")
    return jsonify(success=True)

@app.route('/')
def index():
    return "Welcome to my Flask app!"

@app.route('/api/')
def api_index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
