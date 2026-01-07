import datetime

from eminder.utils import log,debug,info,warning,error,critical
from eminder.db import dbactions



def timed_operation(func, *args, operation_name=None, taskid=None, **kwargs):
    """
    This function originates from my Python teacher Marcus Bellika which I have modified :D  
    Execute a function and measure its execution time.

    Demonstrates:
    - datetime.datetime() for performance measurement
    - Function execution with *args, **kwargs
    - Returning multiple values

    Args:
        func: Function to execute
        *args, **kwargs: Arguments for the function

    Returns:
        Tuple of (result, duration_seconds)
    """
    start_time = datetime.datetime.now()
    result = func(*args, **kwargs)
    finish_time = datetime.datetime.now()

    if operation_name is None:
        operation_name = getattr(func,'__name__', 'unknown')
    
    # Save record for performance in db
    try:
        dbactions.saveperformancerecord(operation_name,start_time,finish_time,taskid)
    except Exception as err:
        error(f'Error when saving to Performance table: {err}')

    duration = (finish_time - start_time).total_seconds()
    return start_time, finish_time, duration

