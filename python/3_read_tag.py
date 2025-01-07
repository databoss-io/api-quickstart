import json
from os import getenv
import requests

# Get our environment configuration -------------------------------------------

# Windows: you can use `set DATABOSS_CLIENT_ID=<value>` to set the environment
# Linux/macOS: you can use `export DATABOSS_CLIENT_ID=<value>` to set the environment
# Repeat the same with the DATABOSS_CLIENT_SECRET, DATABOSS_ORG_ID, and DATABOSS_AGENT_ID
CLIENT_ID = getenv("DATABOSS_CLIENT_ID")
CLIENT_SECRET = getenv("DATABOSS_CLIENT_SECRET")
ORGANIZATION_ID = getenv("DATABOSS_ORG_ID")
AGENT_ID = getenv("DATABOSS_AGENT_ID")
TAG_NAME = input("Name of tag to get: ")


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

get_tag = requests.get(f"https://api-prod.databoss.io/v1/organization/{ORGANIZATION_ID}/agent/{AGENT_ID}/data/{TAG_NAME}/latest", headers={
    "Authorization": f"Bearer {access_token}"
})
get_tag.raise_for_status()
tag_resp = get_tag.json()

# Final output ----------------------------------------------------------------

print("\r\n****** Tag Read *******")
print(json.dumps(tag_resp.get('result'), indent=2))
print("***********************")
