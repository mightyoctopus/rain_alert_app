import kakao_api
import open_weather_api
from datetime import datetime

#-------------------------------------------- Message Scheduling(7AM) -------------------------------------------#

### Currently, time scheduling done by PythonAnywhere Task Scheduler
# def check_time() -> int:
#     current_datetime = datetime.now()
#     current_hour = current_datetime.hour
#     return current_hour


#-------------------------------------------- Operation Logic --------------------------------------------------#

if open_weather_api.check_weather():
    kakao_api.send_message()
    print("Message has been sent successfully.")
else:
    print("It's not supposed to be raining for the next 12 hours.")





