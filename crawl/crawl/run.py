import subprocess
import time

import schedule


def job():
    print("crawling")
    # subprocess.call(["scrapy", "runspider", "hasaki.py"])
    # subprocess.call(["scrapy", "runspider", "pharmacity.py"])
    subprocess.call(["scrapy", "runspider", "guardian.py"])
    # subprocess.call(["scrapy", "runspider", "watson.py"])

schedule.every(1/4).minutes.do(job)

while True:
    schedule.run_pending()
    print("working and waiting")
    time.sleep(5)
