import logging
from flask import Flask, jsonify, request
import stripe
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
import os
from dotenv import load_dotenv

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

def handle_checkout_session_completed(event):
    email = get_email_from_event(event)
    phone_number = get_phone_number_from_event(event)
    logging.debug(f"Extracted email: {email}")
    logging.debug(f"Extracted phone number: {phone_number}")

    if email:
  
        email_content = '''
    <strong>Next Steps:</strong><br>
    1. <a href="https://chat.whatsapp.com/C2EN3GQhQ3d7trKtUCSEFz">Join the WhatsApp  Reception group</a><br>
    2. <a href="https://chat.whatsapp.com/HREyWIoKAJe0FB5o6YfVH9">Join the Group Chat</a><br>
    3. Read the group descriptions, here you will find my info<br>
    4. Message me on WhatsApp with your height, weight, age, and level of fitness. I will respond with a custom diet plan and fitness regiment tailored for you.<br>
    5. From there we will schedule one on one meetings for three month members.
    '''
    send_email(email, 'Welcome to Strong all Along - Your Next Steps', email_content)

    if phone_number:
        send_sms(phone_number, 'Your purchase with Strong all Along is complete! Please check your email for further instructions.')


def register_webhook_routes(app):
    @app.route('/webhook', methods=['POST'])
    def webhook():
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            logging.debug(f"Webhook event received: {event}")

            if event['type'] == 'checkout.session.completed':
                handle_checkout_session_completed(event['data']['object'])
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
