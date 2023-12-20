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

def get_customer_email(payment_intent):
    customer_email = payment_intent.get('receipt_email')
    
    if not customer_email:
        customer_details = payment_intent.get('customer_details')
        if customer_details:
            customer_email = customer_details.get('email')
    
    return customer_email 
#or 'default_email@example.com'

def handle_payment_intent_succeeded(payment_intent):
    logging.debug(f"PaymentIntent succeeded: {payment_intent}")
    customer_email = get_customer_email(payment_intent)
    
    if customer_email is None:
        logging.error("No customer email found for payment intent")
        return
    
    
    #customer_email = "dcarav77@gmail.com"
    send_email(customer_email, 'Payment Successful', '<strong>Thank you for your payment!</strong>')

def handle_payment_intent_failed(payment_intent):
    logging.debug(f"PaymentIntent failed: {payment_intent}")
    customer_email = get_customer_email(payment_intent)
    logging.debug(f"Sending failure email to: {customer_email}")
    send_email(customer_email, 'Payment Failed', '<strong>Your payment failed. Please try again!</strong>')

def register_webhook_routes(app):
    @app.route('/webhook', methods=['POST'])
    def webhook():
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            logging.debug(f"Webhook event received: {event}")

            if event['type'] == 'payment_intent.succeeded':
                handle_payment_intent_succeeded(event['data']['object'])
            elif event['type'] == 'payment_intent.payment_failed':
                handle_payment_intent_failed(event['data']['object'])

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
