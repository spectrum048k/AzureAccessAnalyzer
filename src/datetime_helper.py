import datetime

# function to create starttime and endtime representing the last hour
def get_last_hour():
    now = datetime.datetime.now()
    last_hour = now - datetime.timedelta(hours=1)
    return last_hour, now

# function to create starttime and endtime representing the last day
def get_last_day():
    now = datetime.datetime.now()
    last_day = now - datetime.timedelta(days=1)
    return last_day, now

# function to create starttime and endtime representing the last week
def get_last_week():
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(weeks=1)
    return last_week, now

# function to create starttime and endtime representing now minus N hours
# n must be a positive integer
def get_last_n_hours(n):
    if n < 1:
        raise ValueError('n must be a positive integer')
    
    now = datetime.datetime.now()
    last_n_hours = now - datetime.timedelta(hours=n)
    return last_n_hours, now

