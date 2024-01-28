import logging
import stripe
from flask import jsonify, request

def register_stripe_routes(app, mongo):
    print("Registering stripe routes...")

    @app.route('/api/create-checkout-session', methods=['POST'])
    def create_checkout_session():
        data = request.json
        price_id = data.get('priceId')
        if not price_id:
            return jsonify(error="Missing price ID"), 400

        try:
            session = stripe.checkout.Session.create(
                ui_mode='embedded',
                line_items=[{'price': price_id, 'quantity': 1}],
                mode='payment',
                return_url='http://localhost:3000/return?session_id={CHECKOUT_SESSION_ID}',
                automatic_tax={'enabled': True},
                phone_number_collection={'enabled': True},
            )
            return jsonify(clientSecret=session.client_secret)
        except Exception as e:
            logging.error(f"Error in create_checkout_session: {e}")
            return jsonify(error=str(e)), 403

    @app.route('/api/session-status', methods=['GET'])
    def session_status():
        session_id = request.args.get('session_id')
        if not session_id:
            return jsonify(error="Missing session ID"), 400

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return jsonify({'status': session.status, 'payment_status': session.payment_status})
        except Exception as e:
            logging.error(f"Error in session_status: {e}")
            return jsonify(error=str(e)), 500

    @app.route('/api/opt-in-sms', methods=['POST'])
    def handle_sms_opt_in():
        data = request.json
        session_id = data.get('sessionId')
        opt_in_sms = data.get('optInSMS')
        if session_id and opt_in_sms:
            try:
                mongo.db.opt_in_statuses.insert_one({"session_id": session_id, "opt_in": opt_in_sms})
                return jsonify({"message": "Opt-in status updated"}), 200
            except Exception as e:
                logging.error(f"Error updating opt-in status: {e}")
                return jsonify({"error": str(e)}), 500
        return jsonify({"error": "Invalid request"}), 400
