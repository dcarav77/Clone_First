import os
from flask import Flask, jsonify, request, redirect
import stripe
from flask_cors import CORS  # not sure if I need

# Set your secret key. Remember to switch to your live secret key in production!
stripe.api_key = 'sk_test_51O7mnXEBiprZstxkH0Lhrcv9OGoe1ZiSOHANZvv8L8kICroOFyzVidtNYAau6C3LFtdZAtNy1xStifVvIyKPYAlS00fsbC5wi7'

app = Flask(__name__, static_url_path='', static_folder='public')

YOUR_DOMAIN = 'http://localhost:3000'
CORS(app)  # not sure if I need

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
                    {'price': price_id, 'quantity': 1},
                ],
                mode='payment',
                return_url=YOUR_DOMAIN + '/return?session_id={CHECKOUT_SESSION_ID}',
                automatic_tax={'enabled': True},
            )
            return jsonify(clientSecret=session.client_secret)
        except Exception as e:
            return jsonify(error=str(e)), 403

    @app.route('/session-status', methods=['GET'])
    def session_status():
        session_id = request.args.get('session_id')
        print("Received session_id:", session_id)

        if not session_id:
            return jsonify(error="Missing session ID"), 400

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return jsonify({
                'status': session.status,
                'payment_status': session.payment_status,
            })
        except Exception as e:
            return jsonify(error=str(e)), 500

register_stripe_routes(app)

if __name__ == '__main__':
    app.run()
