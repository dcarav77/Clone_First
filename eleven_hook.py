import logging
from flask import Flask, jsonify, request
import stripe
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Set logging configuration to only log critical errors
logging.basicConfig(level=logging.CRITICAL)

# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

# Stripe and SendGrid configuration
stripe.api_key = os.getenv('STRIPE_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

webhook_app = Flask(__name__)

def send_email(recipient_email, subject, content):
    message = Mail(
        from_email='admin@strongallalong.coach',
        to_emails=recipient_email,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
    except Exception as e:
        pass  # Replaced logging statement with pass

def get_email_from_event(event):
    email = event.get('customer_details', {}).get('email')
    return email

def handle_checkout_session_completed(event):
   
    email = get_email_from_event(event)

    if email:
        send_email(email, 'Purchase Completed', '<strong>Thank you for your purchase!</strong>')
    else:
        pass  

        phone_number = get_phone_number_from_event(event)  # Implement this function
        if phone_number:
                message(phone_number, 'Thank you for your purchase from StrongAllAlong!')

def get_phone_number_from_event(event):
    # Extracting phone number from customer_details within checkout.session
    # Modify this according to where in the event object the phone number is stored
    phone_number = event.get('customer_details', {}).get('phone')
    return phone_number


message = client.messages \
                .create(
                     body="Join earth's mightiest heroes, like Bruce Willis.",
                     from_='+18775406512',
                     to='+407 796 2384'
                 )




def register_webhook_routes(app):
    @app.route('/webhook', methods=['POST'])
    def webhook():
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
           

            if event['type'] == 'checkout.session.completed':
                handle_checkout_session_completed(event['data']['object'])

        except ValueError as e:
            pass  
            return 'Invalid payload', 400
        except stripe.error.SignatureVerificationError as e:
            pass  
            return 'Invalid signature', 400
        except Exception as e:
            pass  
            return jsonify(error=str(e)), 500

        return jsonify(success=True)

if __name__ == '__main__':
    register_webhook_routes(webhook_app)
    webhook_app.run(debug=True)
