from flask import Flask, render_template, send_from_directory
import stripe_routes
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='react_app/build')

CORS(app)

# Register Stripe routes
stripe_routes.register_stripe_routes(app)

@app.route('/')
def index():
    return "Welcome to my Flask app!"

@app.route('/api/')
def api_index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
