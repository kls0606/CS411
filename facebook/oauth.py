 

# Credentials you get from registering a new application
client_id = ' HERE!!!!'
client_secret = 'HERE!!!'

# OAuth endpoints given in the Facebook API documentation
authorization_base_url = 'https://www.facebook.com/dialog/oauth'
token_url = 'https://graph.facebook.com/oauth/access_token'
redirect_uri = 'http://localhost:5000/'     # Should match Site URL

from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
facebook = facebook_compliance_fix(facebook)

# Redirect user to Facebook for authorization
authorization_url, state = facebook.authorization_url(authorization_base_url)
print ('Please go here and authorize,', authorization_url)

# # Get the authorization verifier code from the callback url
# redirect_response = input('http://localhost:5000/')

# # Fetch the access token
# facebook.fetch_token(token_url, client_secret=client_secret,authorization_response=redirect_response)

# # Fetch a protected resource, i.e. user profile
# r = facebook.get('https://graph.facebook.com/me?')
# print (r.content)

import requests

def get_fb_token(app_id, app_secret):
    url = 'https://graph.facebook.com/oauth/access_token'       
    payload = {
        'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret
    }
    response = requests.post(url, params=payload)
    return response.json()['access_token']

print(get_fb_token(client_id,client_secret))
