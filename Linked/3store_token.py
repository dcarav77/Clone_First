import os
import requests
from flask import Flask, jsonify
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# TODO: Replace with a valid access token after user authentication
access_token = 'AQXYsjIMflpcXm6llZ1GeRKUzJNgLJIqqTfWnXAusAY4jJ_ec4iQYyMkpwsevSx4pW8tBygmsL77k5zQtrLD8dsBDBNwDL0AMdE23bAaMUwOfhARNYT0Ezrgfe6OSzyFyztidCZWolzyriIpfM6HzafTWR1xVmvk8QUc9ZU7rurOo_zIjm6-kP1iSNsaqdYscD-x4JvrNu4HxCXnXjcCVePkF1dJCyDVY6YwVLk-qHMJ7bBRQuLMD7PkCoPgNB6j4Rk62WPbogmrrSp0yACjLwNScA9ZXS5LdAxKnvj3qiIcQrSX65fPHvzFzJUUZhJk1ClWj6cwdQoktGrWcHVdR5r2AeILAw'

def get_linkedin_person_id(token):
    url = "https://api.linkedin.com/v2/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("id")
    else:
        logging.error(f"Error fetching LinkedIn Person ID: {response.content}")
        return None

@app.route('/create-linkedin-share', methods=['POST'])
def create_linkedin_share():
    try:
        linkedin_person_id = get_linkedin_person_id(access_token)
        if linkedin_person_id is None:
            return 'Failed to retrieve LinkedIn Person ID', 500

        post_url = 'https://api.linkedin.com/v2/ugcPosts'  # Ensure this is the correct endpoint
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json'
        }

        post_data = {
            # ... existing post_data structure ...
        }

        response = requests.post(post_url, headers=headers, json=post_data)
        
        # Handle the response
        # ... existing response handling ...

    except Exception as e:
        logging.error(f'Error in create_linkedin_share: {str(e)}')
        return 'Failed to create LinkedIn share', 500

if __name__ == '__main__':
    cert_path = '/Users/dustin_caravaglia/Documents/Clone_First/Linked/linkCert.pem'
    key_path = '/Users/dustin_caravaglia/Documents/Clone_First/Linked/linkKey.pem'
    app.run(host='0.0.0.0', port=5001, ssl_context=(cert_path, key_path))

