from datetime import datetime
from time import sleep

start_time = datetime.now()

for i in range(25000):
    pass

sleep(5)
print(datetime.now())
print(int(datetime.now().strftime('%S')) - int(start_time.strftime('%S')))