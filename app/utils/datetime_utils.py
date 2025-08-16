from datetime import datetime,timedelta
from math import floor

def create_timestampt():
    time = datetime.now() + timedelta(days=30)
    return floor(time.timestamp())