import http.client
import webbrowser
from api_credentials import *
from requests.api import request

def prompt_login():
    url = "https://api.dexcom.com/v2/oauth2/login?client_id={0}&redirect_uri={1}&response_type=code&scope=offline_access".format(CLIENT_ID, REDIRECT_URI)
    webbrowser.open(url)

def get_data(auth_code: str):
    conn = http.client.HTTPSConnection("api.dexcom.com")

    payload = "client_secret={0}&client_id={1}&code={2}&grant_type=authorization_code&redirect_uri={3}".format(CLIENT_SECRET, CLIENT_ID, auth_code, REDIRECT_URI)

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    conn.request("POST", "/v2/oauth2/token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return data

def get_egvs(token:str):

    conn = http.client.HTTPSConnection("api.dexcom.com")

    headers = {
        'authorization': "Bearer %s" % token
        }

    conn.request("GET", "/v2/users/self/egvs?startDate=2021-11-01T00:00:00&endDate=2021-11-01T23:59:59", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data


