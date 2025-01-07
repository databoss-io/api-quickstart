import json
from os import getenv
import requests

# Get our environment configuration -------------------------------------------

# Windows: you can use `set DATABOSS_CLIENT_ID=<value>` to set the environment
# Linux/macOS: you can use `export DATABOSS_CLIENT_ID=<value>` to set the environment
# Repeat the same with the DATABOSS_CLIENT_SECRET
CLIENT_ID = getenv("DATABOSS_CLIENT_ID")
CLIENT_SECRET = getenv("DATABOSS_CLIENT_SECRET")

# Get access token ------------------------------------------------------------


get_token = requests.post("https://login.microsoftonline.com/databossio.onmicrosoft.com/oauth2/v2.0/token", data={
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "https://databossio.onmicrosoft.com/api/.default"
})

# Handle if getting the token failed
try:
    get_token.raise_for_status()
except requests.exceptions.HTTPError as err:
    err.add_note(get_token.text)
    raise err

# Get token value
get_token_resp = get_token.json()
access_token = get_token_resp.get("access_token")
if not access_token:
    raise ValueError("Token not returned!")

# Perform test call -----------------------------------------------------------

orgs = requests.get("https://api-prod.databoss.io/v1/organization/mine", headers={
    "Authorization": f"Bearer {access_token}"
})
orgs.raise_for_status()
orgs_resp = orgs.json()

# Final output ----------------------------------------------------------------

print("\r\n****** Granted Organizations *******")
print(json.dumps(orgs_resp.get('result'), indent=2))
print("***********************")
