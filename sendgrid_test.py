import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

os.environ['SENDGRID_API_KEY'] = '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'

message = Mail(
    from_email='admin@strongallalong.coach',
    to_emails='dcarav77@gmail.com',  # replace with your test email
    subject='Testing SendGrid',
    html_content='<strong>Hello, this is a test email!</strong>'
)

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print("Error:", e)
