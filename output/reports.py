import datetime
import mysql.connector
from pathlib import Path

from config import DBCONFIG,PROJECT_ROOT
from modules.logger import log,debug,info,warning,error,critical
from analysis import performance 


def create_report(report_name='Performance report',horizon='Today'):

    date_time = datetime.datetime.now()



    lines = []
    lines.append('='*100)
    lines.append(report_name)
    lines.append(f'Generated: {str(date_time)}.')
    lines.append(f'Horizon: {horizon}.')
    lines.append('='*100)
    lines.append('\n')

    
    if horizon == 'Today':
        horizon = datetime.datetime.now().date()
    else:
        horizon = ''
    

    
    DBConn = mysql.connector.connect(**DBCONFIG);
    cursor = DBConn.cursor(dictionary=True)




    cursor.execute(f'''
    SELECT 
    p.Id,
    p.Operation,
    p.Starttime,
    p.Finishtime,
    SUM(p.Finishtime - p.Starttime) as Operationtime
    FROM Performance as p
    WHERE Starttime LIKE "{horizon}%"
    GROUP BY Id
    Order by Id DESC
    ;
    ''')

    row = cursor.fetchall()

    recordcount = 0
    operationtime = []
    operationtypes = []

    for row in row:
        recordcount+=1
        operationtime.append(row.get('Operationtime'))
        operationtypes.append(row.get('Operation'))
        uniqueoperationtypes = set(operationtypes)


    averagetime = sum(operationtime)/recordcount
    #ageragetimeperoperationtype = 


    lines.append(f'Operation record count: {recordcount}.')
    lines.append(f'Average operation time: {averagetime:.2f} s.')
    lines.append('\n')
    lines.append(f'Operation types:\n {uniqueoperationtypes}.')
    lines.append(f'\n')

    for i in uniqueoperationtypes:
        lines.append(i)
        lines.append


    return '\n'.join(lines)



def save_report_to_file(reportcontent=None, filename=None):
    reports_dir = PROJECT_ROOT / 'reports'
    reports_dir.mkdir(exist_ok=True)

    date = datetime.datetime.now().strftime('%Y%m%d')
    filename = filename + date + '.txt'

    filepath = reports_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(reportcontent)


def DailyReportJob():
    content = create_report(report_name='Daily Performance Report', horizon='Today')
    save_report_to_file(content, filename='DailyPerformanceReport')





if __name__ == '__main__':
    #print(create_report())
    #save_report_to_file(create_report(), filename='DailyPerformanceReport')
    #start_time, finish_time, operation_time = performance.timed_operation(save_report_to_file(create_report(), filename='DailyPerformanceReport'))


    start_time, finish_time, operation_time = performance.timed_operation(DailyReportJob)
    print(f'Start time: {start_time.strftime("%H:%M:%S")}. Finish time: {finish_time.strftime("%H:%M:%S")}')
    print(f'Operation time: {operation_time:.2f} seconds.')