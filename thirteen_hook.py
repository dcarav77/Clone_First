import logging
from flask import Flask, jsonify, request
from pymongo import MongoClient
import stripe
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
import os
from dotenv import load_dotenv
from pymongo import MongoClient



# Setup logging configuration
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

stripe.api_key = os.getenv('STRIPE_API_KEY')

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

webhook_app = Flask(__name__)

def send_email(recipient_email, subject, content):
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        message = Mail(
            from_email='admin@strongallalong.coach',
            to_emails=recipient_email,
            subject=subject,
            html_content=content)
        response = sg.send(message)
        logging.info(f"Email sent to {recipient_email}. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def send_sms(to_number, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        logging.info(f"Attempting to send SMS to {to_number} with body: '{body}'")
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        logging.info(f"SMS sent: SID {message.sid}")
    except Exception as e:
        logging.error(f"Error sending SMS: {e}")

def get_email_from_event(event):
    return event.get('customer_details', {}).get('email')

def get_phone_number_from_event(event):
    return event.get('customer_details', {}).get('phone')

def handle_checkout_session_completed(event, mongo):
    logging.info("Processing checkout session completed event")
    session_id = event.get('id')

    try:
        # Fetch the checkout session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        email = session.get('customer_details', {}).get('email')
        phone_number = session.get('customer_details', {}).get('phone')
        logging.debug(f"Retrieved session data: {session}")
    except Exception as e:
        logging.error(f"Error retrieving Stripe session: {e}")
        return jsonify({"error": str(e)}), 500

    email = session.get('customer_details', {}).get('email')
    phone_number = session.get('customer_details', {}).get('phone')

    logging.info(f"Session ID: {session_id}")
    logging.info(f"Email: {email}")
    logging.info(f"Phone Number: {phone_number}")

    # Check for opt-in status in MongoDB and update with phone number
    opt_in_data = mongo.db.opt_in_statuses.find_one({"session_id": session_id})
    if opt_in_data:
        logging.info(f"Opt-in data retrieved from MongoDB: {opt_in_data}")
        #opt_in_sms = opt_in_data.get('opt_in', False)

    if phone_number:
        result = mongo.db.opt_in_statuses.update_one(
                {"session_id": session_id},
                {"$set": {"phone_number": phone_number}}
            )
        logging.info(f"MongoDB update result: Matched {result.matched_count}, Modified {result.modified_count}")
    else:
        logging.warning(f"No opt-in data found for session ID: {session_id}")
        #opt_in_sms = False

    if email:
            email_content = '''
    <strong>Next Steps:</strong><br>
    1. <a href="https://chat.whatsapp.com/C2EN3GQhQ3d7trKtUCSEFz">Join the WhatsApp  Reception group</a><br>
    2. <a href="https://chat.whatsapp.com/HREyWIoKAJe0FB5o6YfVH9">Join the Group Chat</a><br>
    3. Read the group descriptions, here you will find my info<br>
    4. Message me on WhatsApp with your height, weight, age, and level of fitness. I will respond with a custom diet plan and fitness regiment tailored for you.<br>
    5. From there we will schedule the Zoom Call.
    '''
            send_email(email, 'Welcome to Strong all Along - Your Next Steps', email_content)


    #if phone_number and opt_in_sms:
        #logging.info(f"Preparing to send SMS to {phone_number}")
        #send_sms(phone_number, 'Your purchase with Strong all Along is complete! Please check your email for further instructions.')

    return jsonify(success=True)

        

def register_webhook_routes(app, mongo):
    @app.route('/webhook', methods=['POST'])
    def webhook():
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            logging.debug(f"Webhook event received: {event}")

            if event['type'] == 'checkout.session.completed':
                handle_checkout_session_completed(event['data']['object'], mongo)
        except ValueError as e:
            logging.error("Invalid payload", exc_info=e)
            return 'Invalid payload', 400
        except stripe.error.SignatureVerificationError as e:
            logging.error("Invalid signature", exc_info=e)
            return 'Invalid signature', 400
        except Exception as e:
            logging.error("Unhandled exception", exc_info=e)
            return jsonify(error=str(e)), 500
 
        
        return jsonify(success=True)

#if __name__ == '__main__':
    #register_webhook_routes(webhook_app)
    #webhook_app.run(debug=True)
