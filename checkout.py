from flask import Flask, jsonify, request, redirect
import stripe
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

# Stripe and SendGrid configuration
stripe.api_key = os.getenv('STRIPE_API_KEY')

app = Flask(__name__)

YOUR_DOMAIN = 'http://localhost:3000'  # Replace with your domain

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = request.json
    try:
        payment_intent = stripe.PaymentIntent.create(
            #amount=calculate_order_amount(data['items']),
            currency='usd',
            payment_method_types=['card'],
            receipt_email=data['email']
        )
        return jsonify({'clientSecret': payment_intent['client_secret']})
    except Exception as e:
        return jsonify(error=str(e)), 403


def process_info():
    data = request.json
    
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': data['priceId'], 
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
            customer_email=data['customer_email'],
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)


