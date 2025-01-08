import datetime

def get_last_monday():
    today = datetime.date.today()
    days_to_subtract = today.weekday()
    
    last_monday = today - datetime.timedelta(days=days_to_subtract)
    return last_monday