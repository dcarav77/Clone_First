import os
import requests
from flask import Flask, jsonify
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)

# Hardcoded for demonstration purposes. In a real application, secure this properly.
access_token = ''


def get_linkedin_person_id(token):
    url = "https://api.linkedin.com/v2/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("id")
    else:
        print(f"Error fetching LinkedIn Person ID: {response.content}")
        return None


@app.route('/create-linkedin-share', methods=['POST'])
def create_linkedin_share():
    try:
        linkedin_person_id = get_linkedin_person_id(access_token)
        if linkedin_person_id is None:
            logging.error('Failed to retrieve LinkedIn Person ID')
            return 'Failed to retrieve LinkedIn Person ID', 500

        logging.info(f'Creating LinkedIn share with Person ID: {linkedin_person_id}')

        post_url = 'https://api.linkedin.com/v2/ugcPosts'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json'
        }

        post_data = {
            "author": f"urn:li:person:{linkedin_person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": "Dustin's first post using Linkedin API! yayy"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(post_url, headers=headers, json=post_data)
        
        if response.status_code == 201:
            logging.info('Share created successfully')
            return 'Share created successfully', 201
        else:
            logging.warning(f'Failed to create share: {response.content}')
            return f'Failed to create share: {response.content}', response.status_code

    except Exception as e:
        logging.error(f'Error in create_linkedin_share: {str(e)}')
        return 'Failed to create LinkedIn share', 500



if __name__ == '__main__':
    cert_path = '/Users/dustin_caravaglia/Documents/Clone_First/Linked/linkCert.pem'
    key_path = '/Users/dustin_caravaglia/Documents/Clone_First/Linked/linkKey.pem'
    app.run(host='0.0.0.0', port=5001, ssl_context=(cert_path, key_path))
