import time
import requests

from config import (
    CHECK_INTERVAL_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
    HTTP_TARGETS,
)

from db import init_db, log_status, get_last_status
from notifier import send_telegram
from dashboard import write_dashboard


def check_internet():
    """
    Check internet connectivity using HTTP targets.
    Returns (True/False, reason)
    """
    for url in HTTP_TARGETS:
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            if response.status_code < 500:
                return True, f"OK {url} {response.status_code}"
        except Exception as e:
            last_error = type(e).__name__
            continue

    return False, f"All targets unreachable {last_error if 'last_error' in locals() else ''}".strip()


def main():
    init_db()
    print("UptimePulse started")

    while True:
        online, reason = check_internet()
        status = "UP" if online else "DOWN"

        last_status = get_last_status()

        # log to database
        log_status(status, reason)

        # update dashboard.html
        write_dashboard()

        # notify only if status changed
        if last_status != status:
            message = f"Status changed to {status}\nReason: {reason}"
            send_telegram(message)
            print(message)
        else:
            print(status, reason)

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
