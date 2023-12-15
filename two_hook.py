
import json
import os
import stripe
from flask import Flask, jsonify, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Configure Stripe
stripe.api_key = 'sk_test_51O7mnXEBiprZstxkH0Lhrcv9OGoe1ZiSOHANZvv8L8kICroOFyzVidtNYAau6C3LFtdZAtNy1xStifVvIyKPYAlS00fsbC5wi7'

# Stripe CLI webhook secret for testing
endpoint_secret = 'whsec_78d9d592fcf4f69b9396787a8dfbde16e278f80173737f6e3d0bdb4324ef0b76'

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to my Flask app!"

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook from script 2 triggered")
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        customer_email = payment_intent.get('receipt_email')  # or another email field

        # Send an email using Twilio SendGrid
        send_email(customer_email)

    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

def send_email(recipient_email):
    message = Mail(
        from_email='admin@stronallalong.coach',
        to_emails=recipient_email,
        subject='Yoooooo payment was successful!',
        html_content='<strong>Thank you for your payment!</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    app.run(debug=True)
