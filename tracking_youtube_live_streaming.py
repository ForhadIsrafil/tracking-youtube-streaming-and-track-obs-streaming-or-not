import aiotube
import smtplib
import time
import schedule
from youtube_scraping_api import YoutubeAPI

# ===================UPDATE BY OWNER==================

# ********* CURRENT STREAMING IDS START ******
STREAMING_IDS = []
# ********* CURRENT STREAMING IDS END ********

CHENNEL_ID = "UC-Q"

# SET TIME INTERVAL MINIMUM 5 MINUTE OF MORE
time_interval = 5

# GMAIL CREDENTIALS START
gmail_user = 'your email here'
gmail_app_password = 'app password here'  # app password
receiver_email = 'your receiver email here'
# GMAIL CREDENTIALS END

# ===================UPDATE BY OWNER END===============


# ####################################################################
# ###################### WARNING: DON'T ANYTHING CHANGE BELOW ########
# ####################################################################

off_streams_lists = []

api = YoutubeAPI()


def get_current_streams_ids():
    print("Checking Streaming......")
    live_streaming_list = aiotube.Channel(channel_id=CHENNEL_ID).current_streams()
    print(live_streaming_list)

    # check stream IDs
    for id in live_streaming_list:
        print(api.video(id))
        if id not in STREAMING_IDS and id not in off_streams_lists:
            try:
                print(id)
                # video_metadata = aiotube.Video(str(id))
                video_metadata = api.video(id)
                print(video_metadata)
                send_email(video_data=video_metadata)

                off_streams_lists.append(id)
                print(f"{video_data['title']}. ID: {video_data['id']} not streaming.....!")
            except Exception as e:
                print(e)
                pass


def send_email(video_data):
    print("Sending Email........")
    sender_email = gmail_user
    subject = 'Streaming Email'
    message = f"Subject: {video_data.title}\n\n{video_data.id}"

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(gmail_user, gmail_password)
            smtp.sendmail(sender_email, receiver_email, message)
            print('Email sent successfully!')
    except Exception as e:
        print(e)


# SET TIME INTERVAL MINIMUM 5 MINUTE OF MORE
schedule.every(time_interval).seconds.do(get_current_streams_ids)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)


