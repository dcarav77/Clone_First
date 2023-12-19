'''
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
        except ValueError as e:
            return 'Invalid payload', 400
        except stripe.error.SignatureVerificationError as e:
            return 'Invalid signature', 400

        # Handle different Stripe events
        if event['type'] == 'payment_intent.succeeded':
            handle_payment_intent_succeeded(event['data']['object'])
        elif event['type'] == 'payment_intent.payment_failed':
            handle_payment_intent_failed(event['data']['object'])
        elif event['type'] == 'customer.created':
            pass #something
        elif event['type'] == 'customer.updated':
            pass #something
        elif event['type'] == 'invoice.payment_succeeded':
            pass  # Placeholder for future code
        elif event['type'] == 'invoice.payment_failed':
            pass  # Placeholder for future code
        elif event['type'] == 'subscription.created':
            pass  # Placeholder for future code
        elif event['type'] == 'subscription.updated':
            pass  # Placeholder for future code
        elif event['type'] == 'subscription.deleted':
            pass  # Placeholder for future code
        elif event['type'] == 'product.created':
            pass  # Placeholder for future code
        elif event['type'] == 'product.updated':
            pass  # Placeholder for future code
        elif event['type'] == 'charge.refunded':
            pass  # Placeholder for future code
        elif event['type'] == 'payment_method.attached':
            pass  # Placeholder for future code
        elif event['type'] == 'payment_method.detached':
            pass  # Placeholder for future code
   

        return jsonify(success=True)

    def handle_payment_intent_succeeded(payment_intent):
        customer_email = payment_intent.get('receipt_email') or 'default_email@example.com'
        send_email(customer_email, 'Payment Successful', '<strong>Thank you big Dawg!</strong>')

    def handle_payment_intent_failed(payment_intent):
        customer_email = payment_intent.get('receipt_email') or 'default_email@example.com'
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
            print("Email sent. Status code:", response.status_code)
        except Exception as e:
            print("Error sending email:", e)
'''

   
