import os
from google.oauth2 import service_account
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import json
import time
import schedule
import smtplib
import ftfy

# ===================UPDATE BY OWNER==================
client_id = "83900908707eusercontent.com"
client_secret = "GOCSPYM9Q0XU5X"
client_secrets_file = "client_secret_.apps.googleusercontent.com.json"

# GMAIL CREDENTIALS START
gmail_user = 'your email here'
gmail_app_password = 'ttmnywbgwrtacdct'  # app password
receiver_email = 'your receiver email here'
# GMAIL CREDENTIALS END

# ===================UPDATE BY OWNER END===============

off_streams_lists = []


def get_current_streams(access_token):
    print('get_current_streams............')
    live_stream_url = f"https://www.googleapis.com/youtube/v3/liveStreams?part=id,snippet,status&mine=true&maxResults=20"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    print(off_streams_lists)
    response = requests.get(live_stream_url, headers=headers)
    if response.status_code == 200:
        dic_data = json.loads(response.content)
        for data in dic_data['items']:
            if 'healthStatus' in data['status'] and data['id'] not in off_streams_lists:
                if data['status']['healthStatus']['status'] == 'noData' and data['status'][
                    'streamStatus'] == 'inactive':
                    id = data['id']
                    title = data['snippet']['title']
                    print(title, id)
                    try:
                        email = send_email(title, id)
                        if email:
                            off_streams_lists.append(data['id'])
                    except Exception as e:
                        raise Exception(f"Error : {e}")
    else:
        raise Exception(f"Error : {response.status_code}")


def get_token():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                                                               scopes=scopes)
    flow.run_local_server()

    # token refresh_token
    token = flow.credentials.token
    refresh_token = flow.credentials.refresh_token
    # print(token, refresh_token)

    return token, refresh_token

    # credentials = flow.credentials
    # youtube = googleapiclient.discovery.build(
    #     api_service_name, api_version, credentials=credentials)
    #
    # request = youtube.liveStreams().list(
    #     part="id,status",
    #     id="L-bNJ_vLdTA",
    # )
    # response = request.execute()
    # print(response)


def get_new_token_from_refresh_token(refresh_token):
    """Get a new OAuth 2.0 token from a refresh token."""

    url = "https://oauth2.googleapis.com/token"
    headers = {"Content-Type": "application/json"}
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.content)
        # print(response.json())
        return response_json["access_token"]
    else:
        # print(response.json())
        raise Exception(f"Error getting new token from refresh token: {response.status_code}")


def send_email(title, id):
    print("Sending Email........")
    sender_email = gmail_user

    subject = 'Streaming Email'
    message = ftfy.fix_text(f"Subject: {title}\n\n Stream Key: {id}").encode("utf-8")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(gmail_user, gmail_app_password)
            smtp.sendmail(sender_email, receiver_email, message)
            print('Email sent successfully!')
            return True
    except Exception as e:
        print("send_email:", e)
        return False


if __name__ == "__main__":
    token, refresh_token = get_token()

    while True:
        new_token = get_new_token_from_refresh_token(refresh_token)
        # check streaming...
        get_current_streams(access_token=new_token)
        time.sleep(300)
