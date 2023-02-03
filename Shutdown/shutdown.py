import os
import time
import datetime 

def shutdown(threshold=7):
    now = datetime.datetime.now()
    today7pm = now.replace(hour=19, minute=5, second=0, microsecond=0)
    ct = datetime.datetime.now()
    while ct == today7pm:
        time.sleep(1)  # wait 5 minutes
    os.system("shutdown /s /t 90")

shutdown()
