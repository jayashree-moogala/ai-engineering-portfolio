from datetime import datetime


def get_current_datetime() -> str:
    """Return the current local date and time."""

    # Using astimezone() includes the local timezone offset.
    return datetime.now().astimezone().isoformat(timespec="seconds")
