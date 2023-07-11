from flask import Flask, request
from flask_caching import Cache
import requests
import os
import webbrowser
from urllib.parse import urlencode

app = Flask(__name__)
app.config["SECRET_KEY"] = "any random string"
app.config["CACHE_TYPE"] = "SimpleCache"
cache = Cache(app)

authUri = "https://www.warcraftlogs.com/oauth/authorize"

clientId = os.environ.get('CLIENT_ID')

authPayload = {
    "client_id": clientId,
    "state": "dpaodwpok",
    "redirect_uri": "",
    "response_type": "code"
}

authorize_url_with_params = authUri + "?" + urlencode(authPayload)
webbrowser.open(authorize_url_with_params) 

# called from browser redirect
@app.route("/auth", methods=["GET"])
@cache.cached()
def callback():
    authCode = request.args.get("code")

    tokenUri = "https://www.warcraftlogs.com/oauth/token"

    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")

    response = requests.get("http://localhost:5000/getcode")

    payload = {"redirect_uri": "", "code": authCode, "grant_type": "authorization_code"}

    response = requests.post(tokenUri, data=payload, auth=(client_id, client_secret))
    
    # Check the response status code
    if response.status_code == 200:
        print("POST request was successful!")
        jsonResponse = response.json()
        return jsonResponse
    else:
        print("POST request failed with status code:", response.status_code)
        return f"error: {response.status_code} \n {response.text}"

if __name__ == "__main__":
    app.run()
