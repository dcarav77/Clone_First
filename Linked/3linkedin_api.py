from flask import Flask, request, jsonify
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
port = 5000 

client_id = '78o7h2davl162f'
client_secret = 'm8mMxVdfqe2CyRCo'
redirect_uri = 'https://localhost:5000/auth/linkedin/callback'  # Use your actual domain

# Function to generate LinkedIn Authorization URL
def generate_linkedin_auth_url():
    response_type = 'code'
    state = 'dcarav77'  # Use a unique session state value
    scope = 'openid profile email w_member_social r_liteprofile '
    return f'https://www.linkedin.com/oauth/v2/authorization?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}'

# LinkedIn initiation route
@app.route('/auth/linkedin/initiate', methods=['GET'])
def linkedin_initiate():
    linkedin_authorization_url = generate_linkedin_auth_url()
    logging.info('LinkedIn Authorization URL: %s', linkedin_authorization_url)
    return jsonify({'linkedinAuthorizationUrl': linkedin_authorization_url})

# LinkedIn callback route
@app.route('/auth/linkedin/callback', methods=['GET'])
def linkedin_callback():
    try:
        authorization_code = request.args.get('code')
        state = request.args.get('state')

        access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        grant_type = 'authorization_code'

        access_token_data = {
            'grant_type': grant_type,
            'code': authorization_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri
        }

        response = requests.post(access_token_url, params=access_token_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        access_token = response.json()['access_token']
        expires_in = response.json()['expires_in']
        logging.info('Access Token: %s', access_token)
        logging.info('Expires In (seconds): %s', expires_in)

        api_endpoint = 'https://api.linkedin.com/v2/userinfo'
        api_response = requests.get(api_endpoint, headers={'Authorization': f'Bearer {access_token}'})
        logging.debug('LinkedIn API Response: %s', api_response.json())

        return 'LinkedIn authentication successful'
    except Exception as e:
        logging.error('Error in linkedin_callback: %s', str(e))
        return 'LinkedIn authentication failed', 500

# Root route
@app.route('/', methods=['GET'])
def root():
    return 'Welcome to the root path!'

if __name__ == '__main__':
    cert_path = '/Users/dustin_caravaglia/Documents/Clone_First/Linked/linkCert.pem'
    key_path = '/Users/dustin_caravaglia/Documents/Clone_First/Linked/linkKey.pem'
    app.run(host='0.0.0.0', port=5000, ssl_context=(cert_path, key_path))
