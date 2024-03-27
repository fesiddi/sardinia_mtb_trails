import time

import schedule

from app.segments_stats import fetch_and_write_segments_stats


def job():
    fetch_and_write_segments_stats()


# Schedule the job to run at a specific time every day (e.g., 12:00)
schedule.every().day.at("12:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
