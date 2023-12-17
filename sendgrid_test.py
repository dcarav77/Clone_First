'''
from dotenv import load_dotenv
load_dotenv()  

# Set the absolute path to the .env file
dotenv_path = '/Users/dustin_caravaglia/Documents/Clone_First/sendgrid.env'
load_dotenv(dotenv_path)

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


message = Mail(
    from_email='admin@strongallalong.coach',
    to_emails='dcarav77@gmail.com',  # replace with your test email
    subject='Testing SendGrid',
    html_content='<strong>oh baby this is a test email!</strong>'
)

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print("Error:", e)
'''