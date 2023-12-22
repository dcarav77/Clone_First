import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv('/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env')

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join earth's mightiest heroes, like Bruce Willis.",
                     from_='+18775406512',
                     to='+18548542185'
                 )

print(message.sid)
