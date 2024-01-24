import os
from flask import Flask, jsonify, request, redirect
import requests
import stripe
from flask_cors import CORS

app = Flask(__name__)
port = 5001 

access_token = 'AQXhcFGYAD4QwoCZ3REC-rZ87uGWwTTVASKMvSM7WHB-YLqLCS5GrvyhXEYYv8CfnNMpzCi9NnEPxDmouKO_nuYR_x6o7bsA_zlEDx8CdXZ5vNDPytkaAew4kyOv7ALrFlgidCGOqTZVRr0jwzXA3RwSDwp-hli7rXtSjBojEKiWbYRltVs4tTH57mlvW9hMogzOPO3FYtDkl1bCmSSV9tDs_5m3Nea9y7j1mtOKKTzxDMC6FRqH_cTL9LnWhP00derLRbbylwmkDghL1D8UGO6-hWipxrpIBUC1DUzC2azdLa796kxikxPiBnpXFVXpyVts9raBLTHbrLJNA5IiXHBxKEVaWg'

app = Flask(__name__, static_url_path='', static_folder='public')

@app.route('/create-linkedin-share', methods=['POST'])
def create_linkedin_share():
    try:
        # Retrieve the access token from where you've stored it. 
        access_token = 'AQXhcFGYAD4QwoCZ3REC-rZ87uGWwTTVASKMvSM7WHB-YLqLCS5GrvyhXEYYv8CfnNMpzCi9NnEPxDmouKO_nuYR_x6o7bsA_zlEDx8CdXZ5vNDPytkaAew4kyOv7ALrFlgidCGOqTZVRr0jwzXA3RwSDwp-hli7rXtSjBojEKiWbYRltVs4tTH57mlvW9hMogzOPO3FYtDkl1bCmSSV9tDs_5m3Nea9y7j1mtOKKTzxDMC6FRqH_cTL9LnWhP00derLRbbylwmkDghL1D8UGO6-hWipxrpIBUC1DUzC2azdLa796kxikxPiBnpXFVXpyVts9raBLTHbrLJNA5IiXHBxKEVaWg'

        # Define the API endpoint for creating a share
        post_url = 'https://api.linkedin.com/v2/ugcPosts'

        # Prepare the headers with the access token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json'
        }

        # Prepare the data for the share (customize this as per your requirement)
        post_data = {
            "author": "urn:li:person:YOUR_LINKEDIN_PERSON_ID", #trying to figure out how to get this ID
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


        # Make the POST request to LinkedIn API
        response = requests.post(post_url, headers=headers, json=post_data)

        # Handle the response
        if response.status_code == 201:
            return 'Share created successfully', 201
        else:
            return f'Failed to create share: {response.content}', response.status_code

    except Exception as e:
        print('Error:', str(e))
        return 'Failed to create LinkedIn share', 500

if __name__ == '__main__':

    cert_path = '/Users/dustin_caravaglia/Documents/Clone_First/Linked/linkCert.pem'
    key_path = '/Users/dustin_caravaglia/Documents/Clone_First/Linked/linkKey.pem'

    app.run(host='0.0.0.0', port=5001, ssl_context=(cert_path, key_path))
