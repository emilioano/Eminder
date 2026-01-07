import time
from datetime import datetime,timedelta

from eminder.config import colors
from eminder.services import schedulemanager
from eminder.utils import log,debug,info,warning,error,critical
from eminder.config import SERVICE_REFRESH

def job():
    while 0 < 1:
        schedulemanager.ScheduleManager().run()
        print(f'{colors.OKGREEN}')
        print('='*60)
        print(f'Running the schedule manager as a service (Repeats every {sleep_time} seconds.)')
        date_time = datetime.now()
        next_time = date_time + timedelta(seconds=sleep_time)
        print(f'Last refreshed: {str(date_time).split(".")[0]}')
        print(f'Next refresh:   {str(next_time).split(".")[0]}')
        print('='*60)
        print(f'{colors.ENDC}')
        time.sleep(SERVICE_REFRESH)
        continue



if __name__ == '__main__':
    try:
        job()

    except Exception as err:
        error(f'Schedulerservice stopped with following: {err}')

    except KeyboardInterrupt:
        log(f'Schedulerservice was stopped with keyboard interrupt.')