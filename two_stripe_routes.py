import logging
import stripe
from flask import jsonify, request
from thirteen_hook import send_sms

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
        phone_number = data.get('phoneNumber', None)

        if session_id and opt_in_sms is not None:
            try:
                update_data = {"opt_in": opt_in_sms}
                if phone_number:
                    update_data["phone_number"] = phone_number

                mongo.db.opt_in_statuses.update_one(
                    {"session_id": session_id},
                    {"$set": update_data},
                    upsert=True
                )
                return jsonify({"message": "Opt-in status updated"}), 200
            except Exception as e:
                logging.error(f"Error updating opt-in status: {e}")
                return jsonify({"error": str(e)}), 500
        return jsonify({"error": "Invalid request"}), 400

    @app.route('/api/trigger-sms', methods=['POST'])
    def trigger_sms_notification():
        data = request.json
        session_id = data.get('sessionId')

        if not session_id:
            logging.error("Missing session ID")
            return jsonify(error="Missing session ID"), 400

        logging.info(f"Received session ID for SMS trigger: {session_id}")

        try:
            opt_in_data = mongo.db.opt_in_statuses.find_one({"session_id": session_id})
            logging.info(f"Opt-in data from MongoDB: {opt_in_data}")

            if opt_in_data and opt_in_data.get('opt_in', False):
                phone_number = opt_in_data.get('phone_number')
                logging.info(f"Phone number from opt-in data: {phone_number}")

                if phone_number:
                    send_sms(phone_number, 'Your purchase with Strong all Along is complete!')
                    return jsonify({"message": "SMS notification sent"}), 200
                else:
                    return jsonify({"message": "Phone number not found"}), 404
            else:
                logging.error("Opt-in not found or SMS opt-in is false")
                return jsonify({"message": "Opt-in not found or SMS opt-in is false"}), 404

        except Exception as e:
            logging.error(f"Error in triggering SMS notification: {e}")
            return jsonify({"error": str(e)}), 500
