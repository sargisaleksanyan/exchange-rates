from datetime import datetime, timezone

from zoneinfo import ZoneInfo


def extract_update_date(updated_at_text):
    updated_at_text = updated_at_text.replace("Last updated:", "").replace("\n", "")

    dt = datetime.strptime(
        updated_at_text,
        "%A %d %B %Y %I:%M:%S %p"
    )
    return dt


from datetime import datetime, timezone
from zoneinfo import ZoneInfo

UAE_TZ = ZoneInfo("Asia/Dubai")

def convert_to_utc_time(dt: datetime) -> datetime:
    try:
        if dt.tzinfo is None:
            # assign UAE timezone first
            dt = dt.replace(tzinfo=UAE_TZ)

        # convert to UTC
        return dt.astimezone(timezone.utc)

    except Exception as err:
        print('Error occurred while converting timezone', err)

    return dt

def test_data():
    updated_date = 'Tuesday 14 April 2026 06:05:12 PM'
    date = extract_update_date(updated_date)
    converted_date = convert_to_utc_time(date)
    m = 5

test_data()