import requests
import json
import smtplib
import ftfy


def get_new_token_from_refresh_token(refresh_token):
    """Get a new OAuth 2.0 token from a refresh token."""

    url = "https://oauth2.googleapis.com/token"
    headers = {"Content-Type": "application/json"}
    data = {
        "grant_type": "refresh_token",
        "client_id": '-pip.googleusercontent.com',
        "client_secret": '-oUIrHtQ0XU5X',
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.content)
        print(response.json())

        return response_json["access_token"]
    else:
        print(response.json())
        raise Exception(f"Error getting new token from refresh token: {response.status_code}")




print("Sending Email........")
# sender_email = gmail_user
id = "-015527"
title = "4 h"

# fixed_title = ftfy.fix_text(title)
subject = 'Streaming Email'
message = ftfy.fix_text(f"Subject: {title}\n\n Stream Key: {id}").encode("utf-8")
# message = ftfy.fix_text('4 Nistkästen öffentlich -HQ-oPvL148RmDxpV4jzlQ1619053357015527').encode("utf-8")

# try:
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login("@gmail.com", "")
    smtp.sendmail("@gmail.com", "@gmail.com", message)
    print('Email sent successfully!')
#
# except Exception as e:
#     print("send_email:", e)
