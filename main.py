import subprocess
import sys
from datetime import datetime, timezone

import config


def calculate_nights(first_night_date, today) -> int:
    """first_night_date is the date the FIRST night started.
    Nights elapsed = days since that date."""
    return (today - first_night_date).days


def build_message(nights: int, price_per_night: int, owed_to: str) -> str:
    amount = nights * price_per_night
    return f"☀️ Night {nights} — ₱{amount:,} owed to {owed_to}."


def send_telegram(message: str) -> None:
    try:
        subprocess.run(
            ["/usr/local/bin/hermes", "send", "--to", "telegram", message],
            capture_output=True,
            text=True,
            check=True,
        )
        print("Telegram message sent.")
    except subprocess.CalledProcessError as e:
        print("Failed to send Telegram message.")
        print(e.stderr)
        sys.exit(1)


def main():
    try:
        first_night_date = datetime.strptime(config.FIRST_NIGHT_DATE, "%Y-%m-%d").date()
    except ValueError:
        print(f"FIRST_NIGHT_DATE in config.py is invalid: {config.FIRST_NIGHT_DATE!r}")
        sys.exit(1)

    today = datetime.now(timezone.utc).date()
    nights = calculate_nights(first_night_date, today)

    if nights < 1:
        print(f"First night ({first_night_date}) hasn't started yet. Nothing to send.")
        sys.exit(0)

    message = build_message(nights, config.PRICE_PER_NIGHT, config.OWED_TO)
    print(message)
    send_telegram(message)


if __name__ == "__main__":
    main()