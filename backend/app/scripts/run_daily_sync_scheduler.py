"""Run the AkShare sync job every day at 18:00 Asia/Shanghai.

This script is intentionally separate from the FastAPI app. Keeping the
scheduler outside the web process avoids duplicate jobs when uvicorn reloads
or when multiple backend workers are started.
"""

from apscheduler.schedulers.blocking import BlockingScheduler

from app.scripts.sync_akshare_data import main as sync_akshare_data

SYNC_HOUR = 18
SYNC_MINUTE = 0
TIMEZONE = "Asia/Shanghai"


def run_sync_job() -> None:
    sync_akshare_data()


def main() -> None:
    scheduler = BlockingScheduler(timezone=TIMEZONE)
    scheduler.add_job(
        run_sync_job,
        trigger="cron",
        hour=SYNC_HOUR,
        minute=SYNC_MINUTE,
        id="daily-akshare-sync",
        replace_existing=True,
    )
    print(f"AkShare sync scheduler started: every day {SYNC_HOUR:02d}:{SYNC_MINUTE:02d} {TIMEZONE}")
    scheduler.start()


if __name__ == "__main__":
    main()
