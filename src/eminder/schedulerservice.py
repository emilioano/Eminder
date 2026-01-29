import time
import threading
from datetime import datetime,timedelta

from eminder.config import colors
from eminder.services import schedulemanager
from eminder.services import visualization
from eminder.utils import log,debug,info,warning,error,critical
from eminder.config import SERVICE_REFRESH,REPORT_REFRESH

sleep_time = SERVICE_REFRESH
report_sleep_time = REPORT_REFRESH

status_lock = threading.Lock()
stop_event = threading.Event()

status = {
    'schedulerjob': {'lastrun':None, 'nextrun':None},
    'reportjob': {'lastrun':None, 'nextrun':None}
}


def schedulerjob():
    retries = 0
    retry_interval = 1
    exhaust = 10
    while not stop_event.is_set():
        try:
            schedulemanager.ScheduleManager().run()

            now = datetime.now()

            status['schedulerjob']['lastrun'] = now
            status['schedulerjob']['nextrun'] = now + timedelta(seconds=sleep_time)

            information()
            retries = 0
            retry_interval = 1

            if stop_event.wait(SERVICE_REFRESH):
                break

        except Exception as err:
            retries+=1
            error(f'Schedulerjob stopped with following: {err}')
            error(f'Will wait {retry_interval} seconds and then try again. Retry attempt {retries} of {exhaust}.')
            retry_interval*=2

            if stop_event.wait(retry_interval):
                break
            
            if retries >= exhaust:
                break


def reportjob():
    retries = 0
    retry_interval = 1
    exhaust = 10

    while not stop_event.is_set():
        try:
            visualization.runreports()

            now = datetime.now()
            status['reportjob']['lastrun'] = now
            status['reportjob']['nextrun'] = now + timedelta(seconds=report_sleep_time)

            information()
            retries = 0
            retry_interval = 1

            if stop_event.wait(REPORT_REFRESH):  
                break      
            
        except Exception as err:
            retries+=1
            error(f'Reportjob stopped with following: {err}')
            error(f'Will wait {retry_interval} seconds and then try again. Retry attempt {retries} of {exhaust}.')
            retry_interval*=2

            if stop_event.wait(retry_interval):
                break

            if retries >= exhaust:
                break


def information():
    with status_lock:
        s1 = status['schedulerjob']
        if s1['lastrun'] is not None:
            print(f'{colors.OKGREEN}')
            print('='*60)
            print(f'Running the schedule manager as a service (Repeats every {sleep_time} seconds.)')
            print(f'Last refreshed: {s1["lastrun"]:%Y-%m-%d %H:%M:%S}')
            print(f'Next refresh:  {s1["nextrun"]:%Y-%m-%d %H:%M:%S}')
            print('='*60)
            print(f'{colors.ENDC}')

        s2 = status ['reportjob']
        if s2['lastrun'] is not None:
            print(f'{colors.OKBLUE}')
            print('='*60)
            print(f'Generating visual reports every {report_sleep_time} seconds.)')
            print(f'Last refreshed: {s2["lastrun"]:%Y-%m-%d %H:%M:%S}')
            print(f'Next refresh:  {s2["nextrun"]:%Y-%m-%d %H:%M:%S}')
            print('='*60)
            print(f'{colors.ENDC}')


def job():

    thread2 = threading.Thread(target=schedulerjob)
    thread1 = threading.Thread(target=reportjob)
    thread1.start()
    thread2.start()

    try:
        while thread1.is_alive() or thread2.is_alive():
            thread1.join(timeout=0.5)
            thread2.join(timeout=0.5)
    except KeyboardInterrupt:
        print("Ctrl + C detected - stopping...")
        stop_event.set()
        for _ in range(20):
            if not (thread1.is_alive() or thread2.is_alive()):
                break
            thread1.join(timeout=0.5)
            thread2.join(timeout=0.5)

if __name__ == '__main__':
    try:
        job()

    except Exception as err:
        error(f'Schedulerservice stopped with following: {err}')

    except KeyboardInterrupt:
        log(f'Schedulerservice was stopped with keyboard interrupt.')
        stop_event.set()