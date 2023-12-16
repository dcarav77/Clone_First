from flask import Flask, jsonify, request
import stripe
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

# Stripe and SendGrid configuration
stripe.api_key = 'sk_test_51O7mnXEBiprZstxkH0Lhrcv9OGoe1ZiSOHANZvv8L8kICroOFyzVidtNYAau6C3LFtdZAtNy1xStifVvIyKPYAlS00fsbC5wi7'
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

app = Flask(__name__)

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

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        customer_email = payment_intent.get('receipt_email') or 'dcarav77@gmail.com'  # Replace with your test email
        send_email(customer_email)

    return jsonify(success=True)

def send_email(recipient_email):
    message = Mail(
        from_email='admin@strongallalong.coach',
        to_emails=recipient_email,
        subject='Payment was successful!',
        html_content='<strong>Thank you for your payment!</strong>')
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email sent. Status code:", response.status_code)
    except Exception as e:
        print("Error sending email:", e)

if __name__ == '__main__':
    app.run(debug=True)
