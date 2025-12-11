import datetime
import mysql.connector

from config import DBCONFIG
from modules.logger import log,debug,info,warning,error,critical



def timed_operation(func, *args, operation_name=None, taskid=None, **kwargs):
    """
    This function originates from my Python teacher Marcus Bellika :D 
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
    
    DBConn = mysql.connector.connect(**DBCONFIG);
    cursor = DBConn.cursor(dictionary=True)

    sql = 'INSERT INTO Performance(Operation,Starttime,Finishtime,TaskId) VALUES(%s,%s,%s,%s)'
    
    try:
        cursor.execute(sql, (operation_name,start_time,finish_time,taskid))
        DBConn.commit()
    except Exception as err:
        error('Error when saving to Performance table: {err}')

    duration = (finish_time - start_time).total_seconds()
    return start_time, finish_time, duration

