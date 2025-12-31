import time
from datetime import datetime,timedelta

from config import colors
from modules import schedulemanager
from modules.logger import log,debug,info,warning,error,critical

sleep_time = 15


def job():
    while 0 < 1:
        schedulemanager.event_trigger()
        print(f'{colors.OKGREEN}')
        print('='*60)
        print(f'Running the schedule manager as a service (Repeats every {sleep_time} seconds.)')
        date_time = datetime.now()
        next_time = date_time + timedelta(seconds=sleep_time)
        print(f'Last refreshed: {str(date_time).split(".")[0]}')
        print(f'Next refresh:   {str(next_time).split(".")[0]}')
        print('='*60)
        print(f'{colors.ENDC}')
        time.sleep(sleep_time)
        continue



if __name__ == '__main__':
    try:
        job()

    except Exception as err:
        error(f'Schedulerservice stopped with following: {err}')

    except KeyboardInterrupt:
        log(f'Schedulerservice was stopped with keyboard interrupt.')