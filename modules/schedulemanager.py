import mysql.connector
import json
import datetime

EmilsSchedulerDB = mysql.connector.connect(host='localhost',user='root',password='0popcorn0',database='EmilsSchedulerDB');
cursor = EmilsSchedulerDB.cursor(dictionary=True)


def event_trigger():
    #now_str = str(datetime.datetime.now())
    #date_time = (now_str.split('.')[0])

    #date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    date_time = datetime.datetime.now()

    print(f' Nuvarande tid: {date_time}.')

    


    cursor.execute('SELECT * FROM Tasks')
    dbpost = cursor.fetchall()   

    for dbpost in dbpost:
        #print(dbpost)

        if (dbpost.get('Active')) == 1:
            #print(f'{dbpost.get("Schedule")}.')

            schedule_raw = dbpost.get('Schedule')
            schedule = json.loads(schedule_raw)
            print(schedule)

            schedule_type = schedule['type']
            last_triggered = dbpost.get('Lasttriggered') 

            trigger_time = schedule['time']

            # Apply different datetime logic depending on the Schedule Type

            if schedule_type == 'once':
                trigger_dt = datetime.datetime.strptime(trigger_time, "%Y-%m-%d %H:%M")  
            else:
                trigger_dt = datetime.datetime.strptime(trigger_time, "%H:%M")


            taskid = dbpost.get('TaskId')

            print(f'Taskid: {taskid}')
            print(f'Schedule type: {schedule_type}')
            print(f'Trigger time: {trigger_dt}')

            #yesterday_dt = datetime.datetime.now() - datetime.timedelta(days=1)
            #yesterday = yesterday_dt.strftime('%Y-%m-%d')
            #print(f'Gårdagens datum: {yesterday}')
            
            today = datetime.datetime.now().date()
            #today = today_dt.strptime('%Y-%m-%d')
            print(f'Dagens datum: {today}')
            
            # Apply different calculation logic depending on the Schedule Type

            if schedule_type == 'once' and trigger_time:
                print('Schedule type is Once!')

                print(f'Trigger time: {trigger_dt}. Now time: {date_time}')
                if trigger_dt <= date_time and last_triggered is None:
                    print('Trigger hit!!')

                    # Send to message_out!!

                    insert_last_triggered = 'UPDATE Tasks SET Lasttriggered = %s WHERE Taskid = %s;'
                    cursor.execute(insert_last_triggered, (date_time,taskid))
                    EmilsSchedulerDB.commit()
                    print(f'Last triggered updated! On id {taskid}.')

            elif schedule_type == 'daily' and trigger_time:
                print('Schedule type is Daily!')
                print(f'Trigger time: {trigger_dt}. Now time: {date_time}')
                if (trigger_dt <= date_time) and (last_triggered is None or last_triggered.date() < today):
                #if trigger_dt <= date_time and last_triggered is None:
                    print('Trigger hit!!')
                    # Send to message_out!!
                    insert_last_triggered = 'UPDATE Tasks SET Lasttriggered = %s WHERE Taskid = %s;'
                    cursor.execute(insert_last_triggered, (date_time,taskid))
                    EmilsSchedulerDB.commit()
                    print(f'Last triggered updated! On id {taskid}.')

            elif schedule_type == 'weekly' and trigger_time:
                print('Schedule type is Weekly!')

                current_weekday = datetime.datetime.now().weekday()

                days_map = {
                    0:'mon',
                    1:'tue',
                    2:'wed',
                    3:'thu',
                    4:'fri',
                    5:'sat',
                    6:'sun'
                }

                day = days_map[current_weekday]

                print(f'Idag med tre bokstäver: {day}')

                print(f'Veckodag: {current_weekday}')
                print(f'Trigger time: {trigger_dt}. Now time: {date_time}')
                if (trigger_dt <= date_time) and (last_triggered is None or last_triggered.date() < today):
                #if trigger_dt <= date_time and last_triggered is None:
                    print('Trigger hit!!')
                    # Send to message_out!!
                    insert_last_triggered = 'UPDATE Tasks SET Lasttriggered = %s WHERE Taskid = %s;'
                    cursor.execute(insert_last_triggered, (date_time,taskid))
                    EmilsSchedulerDB.commit()
                    print(f'Last triggered updated! On id {taskid}.')                    

                
            



event_trigger()