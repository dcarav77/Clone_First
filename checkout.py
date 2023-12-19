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


