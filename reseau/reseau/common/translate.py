import arrow
from datetime import datetime


def format_to_date(datetime: datetime):
    # Convert the datetime to an arrow object
    ar = arrow.get(datetime)

    return ar.format('D MMMM YYYY', locale='fr_FR')


def from_now(datetime: datetime):
    # Convert the datetime to an arrow object
    ar = arrow.get(datetime)

    return ar.humanize(locale='fr_FR')
