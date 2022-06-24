import datetime


def get_current_week_as_range():
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)
    return (start_week, end_week)
