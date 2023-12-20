import logging
from flask import Flask, jsonify, request
import stripe
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

# Setup basic logging configuration
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

# Stripe and SendGrid configuration
stripe.api_key = os.getenv('STRIPE_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

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
        logging.info(f"Email sent to {recipient_email}. Status code: {response.status_code}")
        logging.debug(f"SendGrid response body: {response.body}")
    except Exception as e:
        logging.error(f"Error sending email to {recipient_email}", exc_info=True)

def get_email_from_event(event):
     # Extracting email from customer_details within checkout.session
    email = event.get('customer_details', {}).get('email')
    return email

def handle_checkout_session_completed(event):
    logging.debug(f"Checkout session completed: {event}")
    
    # Detailed logging
    logging.debug("Customer details: {}".format(event.get('customer_details')))
    logging.debug("Billing details: {}".format(event.get('billing_details')))

    email = get_email_from_event(event)

    if email:
        send_email(email, 'Purchase Completed', '<strong>Thank you for your purchase!</strong>')
    else:
        logging.error("No email found in checkout session")

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
            logging.error("Invalid payload received", exc_info=True)
            return 'Invalid payload', 400
        except stripe.error.SignatureVerificationError as e:
            logging.error("Invalid signature", exc_info=True)
            return 'Invalid signature', 400
        except Exception as e:
            logging.error("Unhandled exception", exc_info=True)
            return jsonify(error=str(e)), 500

        return jsonify(success=True)

if __name__ == '__main__':
    register_webhook_routes(webhook_app)
    webhook_app.run(debug=True)
