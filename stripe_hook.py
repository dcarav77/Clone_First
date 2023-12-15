'''
import json
import os
import stripe

from flask import Flask, jsonify, request

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = "sk_test_51O7mnXEBiprZstxkH0Lhrcv9OGoe1ZiSOHANZvv8L8kICroOFyzVidtNYAau6C3LFtdZAtNy1xStifVvIyKPYAlS00fsbC5wi7"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_78d9d592fcf4f69b9396787a8dfbde16e278f80173737f6e3d0bdb4324ef0b76'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
      invoice = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)
'''