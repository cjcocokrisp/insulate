import http.client
import webbrowser
from api_credentials import *
from requests.api import request
import json

# For this module to work an api_credentials.py file is needed and must contain valid API credentials. 

def prompt_login():
    
    "Opens the web browser to the sign in page."
    
    url = "https://api.dexcom.com/v2/oauth2/login?client_id={0}&redirect_uri={1}&response_type=code&scope=offline_access".format(CLIENT_ID, REDIRECT_URI)
    webbrowser.open(url)

def get_bearer(auth_code: str):
    conn = http.client.HTTPSConnection("api.dexcom.com")

    payload = "client_secret={0}&client_id={1}&code={2}&grant_type=authorization_code&redirect_uri={3}".format(CLIENT_SECRET, CLIENT_ID, auth_code, REDIRECT_URI)

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    conn.request("POST", "/v2/oauth2/token", payload, headers) # Requets bearer token from API. 

    res = conn.getresponse()
    data = res.read()

    bearer = json.loads(data) # Converts the output to something useable by the program. 

    return bearer

def get_egvs(token:str, start_date:str, end_date:str):

    conn = http.client.HTTPSConnection("api.dexcom.com")

    headers = {
        'authorization': "Bearer %s" % token # Uses the bearer that was obtained from get_bearer(). 
        }

    conn.request("GET", "/v2/users/self/egvs?startDate=" + start_date + "&endDate=" + end_date, headers=headers) # Formats API request based on the given start and end dates and then makes the request. 

    res = conn.getresponse() 
    data = res.read()

    egvs = json.loads(data) # converts output to somethign useable by the program. 

    return egvs



