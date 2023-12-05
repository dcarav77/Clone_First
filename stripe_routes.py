import os
from flask import Flask, jsonify, redirect, request
import stripe

# Configure Stripe Python SDK
stripe.api_key = 'sk_test_51O7mnXEBiprZstxkH0Lhrcv9OGoe1ZiSOHANZvv8L8kICroOFyzVidtNYAau6C3LFtdZAtNy1xStifVvIyKPYAlS00fsbC5wi7'

app = Flask(__name__, static_url_path='', static_folder='public')
YOUR_DOMAIN = 'http://localhost:3000'

def register_stripe_routes(app):
    @app.route('/create-checkout-session', methods=['POST'])
    def create_checkout_session():
        data = request.json
        price_id = data.get('priceId')  

        if not price_id:
            return jsonify(error="Missing price ID"), 400

        try:
            session = stripe.checkout.Session.create(
                ui_mode='embedded',
                line_items=[
                    {
                        'price': price_id,  
                        'quantity': 1,
                    },
                ],
                mode='payment', 
                return_url=YOUR_DOMAIN + '/return',
                automatic_tax={'enabled': True},
            )
            return jsonify(clientSecret=session.client_secret)
        except Exception as e:
            return jsonify(error=str(e)), 403

    # Include other routes here, such as /session-status from the first script

register_stripe_routes(app)


