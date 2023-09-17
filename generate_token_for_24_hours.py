import requests
import json


def get_token(client_id, client_secret, expires_in):
    """Get an OAuth 2.0 token."""
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    url = "https://oauth2.googleapis.com/token"
    headers = {"Content-Type": "application/json"}
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": scopes,
        "expires_in": expires_in
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.content)
        print(response.json())
        return response_json["access_token"]
    else:
        print(response.json())
        raise Exception(f"Error getting token: {response.status_code}")


if __name__ == "__main__":
    client_id = "'839009087076oogleusercontent.com'"
    client_secret = 'GOCSPX-Q0XU5X'
    expires_in = 86400  # 24 hours

    access_token = get_token(client_id, client_secret, expires_in)

    print(f"Access token: {access_token}")
