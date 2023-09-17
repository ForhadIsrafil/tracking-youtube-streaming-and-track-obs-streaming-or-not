import psutil
import os
import subprocess
import time



def is_obs_streaming():
    pid = None
    # Check if OBS is running
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'obs' in proc.info['name'].lower():
            # print(proc.info)
            pid = proc.info['pid']
            # print(pid, proc.info['name'].lower())

            # Check for network connections (assuming streaming uses a specific port)
            for conn in psutil.net_connections(kind='tcp'):
                if conn.status == psutil.CONN_ESTABLISHED and conn.pid == pid:
                    print(conn.status, conn.laddr.port)
                    # if conn.laddr.port == 4455:  # Replace with the streaming port
                    return True, pid
    return False, pid


while True:
    status, pid = is_obs_streaming()
    if status:
        # print("OBS is actively streaming.")
        pass
    else:
        print("OBS is not streaming.")
        try:
            # Define the command to close OBS
            close_command = "taskkill /f /im obs64.exe"
            # Close OBS
            subprocess.run(close_command)
        except Exception as e:
            print(e)

        # Start OBS
        os.chdir("C:\\Program Files\\obs-studio\\bin\\64bit\\")
        os.system("start obs64.exe")
        print("Opening the OBS Software.....")
    # Wait for OBS to terminate (adjust the timeout as needed)
    timeout = 300  # 300 seconds == 5 minute
    time.sleep(timeout)


# if no data is sending to YouTube
# I use a *.bat with this text to terminate OBS after a crash
# terminate the OBS process and restart
# want to "Close OBS" and "Restart OBS" software by the python bot/script