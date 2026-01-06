import datetime
from pathlib import Path

from eminder.config import PROJECT_ROOT
from eminder.utils import log,debug,info,warning,error,critical
from eminder.analysis import performance 
from eminder.db import dbactions


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
    

    row = dbactions.fetchperformancerecords(horizon)

    recordcount = 0
    operationtime = []
    operationtypes = []

    operations = []

    time_per_operation = 0



    for row in row:
        try:
            recordcount+=1
            operationid = row.get('Id')
            operationtime.append(row.get('Operationtime'))
            operationtypes.append(row.get('Operation'))
            uniqueoperationtypes = set(operationtypes)

            operations.append({
                'id':operationid,
                'recordnumber':recordcount,
                'operation':row.get('Operation'),
                'time':row.get('Operationtime')
                })


        except Exception as err:
            error(err)
            break

    averagetime = sum(operationtime)/recordcount

    lines.append(f'Operation record count: {recordcount}.')
    lines.append(f'Average operation time: {averagetime:.2f} s.')
    lines.append('\n')
    lines.append(f'Operation types:\n {uniqueoperationtypes}.')
    lines.append(f'\n')

    lines.append(f'Performance per operation:')

    for i in uniqueoperationtypes:
        try:
            lines.append(i)
            times = [op["time"] for op in operations if op["operation"] == i]
            time_per_operation = sum(times)
            count_per_operation = len(times)
            average_per_operation = time_per_operation / len(times)
            max_per_operation = max(times)
            min_per_operation = min(times)

            lines.append(f'     Count: {count_per_operation}.')
            lines.append(f'     Total time spent: {str(time_per_operation)} s')
            lines.append(f'     Average time: {average_per_operation:.2f} s.')
            lines.append(f'     Max time: {max_per_operation:.2f} s.')
            lines.append(f'     Min time: {min_per_operation:.2f} s.')
            lines.append(f'\n')

            
        except Exception as err:
            error(err)
            break

    return '\n'.join(lines)



def save_report_to_file(reportcontent=None, filename=None):
    reports_dir = PROJECT_ROOT / 'reports'
    reports_dir.mkdir(exist_ok=True)

    date = datetime.datetime.now().strftime('%Y%m%d')
    filename = filename + date + '.txt'

    filepath = reports_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(reportcontent)


def dailyreportjob():
    content = create_report(report_name='Daily Performance Report', horizon='Today')
    save_report_to_file(content, filename='DailyPerformanceReport')





if __name__ == '__main__':
    start_time, finish_time, operation_time = performance.timed_operation(dailyreportjob)
    print(f'Start time: {start_time.strftime("%H:%M:%S")}. Finish time: {finish_time.strftime("%H:%M:%S")}')
    print(f'Operation time: {operation_time:.2f} seconds.')