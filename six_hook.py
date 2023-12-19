'''
import logging
from flask import Flask, jsonify, request
import stripe
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

# Stripe and SendGrid configuration
stripe.api_key = os.getenv('STRIPE_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

webhook_app = Flask(__name__)

def register_webhook_routes(app):
    @app.route('/webhook', methods=['POST'])
    def webhook():
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = 'whsec_78d9d592fcf4f69b9396787a8dfbde16e278f80173737f6e3d0bdb4324ef0b76'
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            logging.debug(f"Webhook event received: {event}")
        except ValueError as e:
            return 'Invalid payload', 400
        except stripe.error.SignatureVerificationError as e:
            return 'Invalid signature', 400

        # Handle different Stripe events
        if event['type'] == 'payment_intent.succeeded':
            handle_payment_intent_succeeded(event['data']['object'])
        elif event['type'] == 'payment_intent.payment_failed':
            handle_payment_intent_failed(event['data']['object'])
        # ... other event types ...

        return jsonify(success=True)

    def handle_payment_intent_succeeded(payment_intent):
        logging.debug(f"PaymentIntent succeeded: {payment_intent}")
        # customer_email = payment_intent.get('receipt_email') or 'default_email@example.com'
        customer_email = "dcarav77@gmail.com"
        logging.debug(f"Sending success email to: {customer_email}")
        send_email(customer_email, 'Payment Successful', '<strong>Thank you big Dawg!</strong>')

    def handle_payment_intent_failed(payment_intent):
        logging.debug(f"PaymentIntent failed: {payment_intent}")
        customer_email = payment_intent.get('receipt_email') or 'default_email@example.com'
        
        if not customer_email:
            customer_email = 'default_email@example.com'
            logging.debug("No receipt email found in payment_intent, using default.")
        
        
        logging.debug(f"Sending failure email to: {customer_email}")
        send_email(customer_email, 'Payment Failed', '<strong>Your payment failed. Please try again!</strong>')

    def send_email(recipient_email, subject, content):
        message = Mail(
            from_email='admin@strongallalong.coach',
            to_emails=recipient_email,
            subject=subject,
            html_content=content)
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            logging.info(f"Email sent. Status code: {response.status_code}")
        except Exception as e:
            logging.error(f"Error sending email: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    webhook_app.run(debug=True)
'''