import mysql.connector
import json
import datetime

from modules.logger import log,debug,info,warning,error,critical
from config import DBCONFIG,colors
from output import mail_out, discord_out
from analysis import performance



#print(os.getcwd())

def event_trigger():

    def Schedulerjob():

        DBConn = mysql.connector.connect(**DBCONFIG);
        cursor = DBConn.cursor(dictionary=True)

        #now_str = str(datetime.datetime.now())
        #date_time = (now_str.split('.')[0])

        #date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        date_time = datetime.datetime.now()

        #print(f' Nuvarande tid: {date_time}.')


        cursor.execute('''
        SELECT 
        tr.*, 
        t.*, 
        r.* 
        FROM Taskrecipients AS tr 
        INNER JOIN Tasks as t on tr.Taskid = t.Taskid 
        INNER JOIN Recipients as r on tr.RecipientId = r.RecipientId
        ORDER BY t.TaskId ASC;
        ''')

        row = cursor.fetchall()   

        for row in row:

            def Messageout():
                # Send to message_out!!
                if channel == 1:
                    mail_out.gmail_send_message(recipient_email,mail_subject,task_message) 
                elif channel == 3:
                    discord_out.discord_send_message(recipient_discordhook, mail_subject + ': ' + task_message)
                elif channel == 3:
                    mail_out.gmail_send_message(recipient_email,mail_subject,task_message)
                    discord_out.discord_send_message(recipient_discordhook, mail_subject + ': ' + task_message)


            if (row.get('Active')) == 1:
                #print(f'{row.get("Schedule")}.')

                schedule_raw = row.get('Schedule')
                schedule = json.loads(schedule_raw)



                schedule_type = schedule['type']
                last_triggered = row.get('Lasttriggered') 
                created_at = row.get('Createdtime')
                trigger_time = schedule['time']
                channel = row.get('Channel')


                task_message = 'Alert from Eminder at' + trigger_time + '. ' + row.get('Message')
                recipient_id = row.get('RecipientId')
                recipient_name = row.get('Name')
                recipient_email = row.get('Email')
                recipient_phone = row.get('Phone')
                recipient_discordhook = row.get('DiscordHook')

                
                mail_subject = row.get('Subject') 
                if mail_subject is None:
                    mail_subject = f'Alert from Eminder to {recipient_name}!'

                # Apply different datetime logic depending on the Schedule Type.
                # If type 'once' we check both date and time, else only time, date will be checked separately.
                if schedule_type == 'once':
                    trigger_dt = datetime.datetime.strptime(trigger_time, "%Y-%m-%d %H:%M") 
                else:
                    trigger_dt = datetime.datetime.strptime(trigger_time, "%H:%M").time()


                taskid = row.get('TaskId')

                print('='*60)
                print(f'Taskid: {taskid}')
                #print(f'Schedule type: {schedule_type}')
                #print(f'Scheduled time: {trigger_dt}')
                #print(schedule)
                print(f'RecipientId: {recipient_id}. Recipient name: {recipient_name}. Recipient e-mail: {recipient_email}. Recipient_phone: {recipient_phone}.')
                if mail_subject is not None:
                    print(f'Subject: {mail_subject}')
                print(f'Message: {task_message}')

                #yesterday_dt = datetime.datetime.now() - datetime.timedelta(days=1)
                #yesterday = yesterday_dt.strftime('%Y-%m-%d')
                #print(f'Gårdagens datum: {yesterday}')

                today = datetime.datetime.now().date()
                #today = today_dt.strptime('%Y-%m-%d')
                #print(f'Dagens datum: {today}')


                # Apply different calculation logic depending on the Schedule Type

                if schedule_type == 'once' and trigger_time:
                    print('Schedule type is Once!')

                    print(f'Trigger time: {trigger_dt}. Now time: {date_time}')
                    if trigger_dt <= date_time and last_triggered is None:
                        print('Trigger hit!!')

                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')


                        insert_last_triggered = 'UPDATE Tasks SET Lasttriggered = %s WHERE Taskid = %s;'
                        cursor.execute(insert_last_triggered, (date_time,taskid))
                        DBConn.commit()
                        log(f'Last triggered updated to {date_time} On TaskId {taskid}.')

                elif schedule_type == 'daily' and trigger_time:
                    print('Schedule type is Daily!')
                    print(f'Trigger time: {trigger_dt}. Now time: {date_time}')
                    if (trigger_dt <= date_time.time()) and (last_triggered is None or last_triggered.date() < today):

                        print('Trigger hit!!')
                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')


                        insert_last_triggered = 'UPDATE Tasks SET Lasttriggered = %s WHERE Taskid = %s;'
                        cursor.execute(insert_last_triggered, (date_time,taskid))
                        DBConn.commit()
                        log(f'Last triggered updated to {date_time} On TaskId {taskid}.')

                elif schedule_type == 'monthly' and trigger_time:
                    print('Schedule type is Monthly!')

                    trigger_days = int(schedule['days'])
                    current_weekday = int(datetime.datetime.now().day)  


                    print(f'Idag i siffror: {current_weekday}')

                    print(f'Trigger time: {trigger_dt}. Now time: {date_time}')

                    print(f'Trigger-dagar: {trigger_days}')


                    #if (trigger_dt <= date_time) and (last_triggered is None or last_triggered.date() < today):
                    if (current_weekday == trigger_days) and (trigger_dt <= date_time.time()) and (last_triggered is None or last_triggered.date() < today):
                        print('Trigger hit!!')

                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')

                        insert_last_triggered = 'UPDATE Tasks SET Lasttriggered = %s WHERE Taskid = %s;'
                        cursor.execute(insert_last_triggered, (date_time,taskid))
                        DBConn.commit()
                        log(f'Last triggered updated to {date_time} On TaskId {taskid}.')


                elif schedule_type == 'weekly' and trigger_time:
                    print('Schedule type is Weekly!')

                    trigger_days = schedule['days']
                    current_weekday = datetime.datetime.now().weekday()
                    #trigger_fire = datetime.datetime.combine(today,trigger_dt)


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

                    print(f'Trigger time: {trigger_dt}. Now time: {date_time}')

                    print(f'Trigger-dagar: {trigger_days}')


                    #if (trigger_dt <= date_time) and (last_triggered is None or last_triggered.date() < today):
                    if (day in trigger_days) and (trigger_dt <= date_time.time()) and (last_triggered is None or last_triggered.date() < today):
                        print('Trigger hit!!')

                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')

                        insert_last_triggered = 'UPDATE Tasks SET Lasttriggered = %s WHERE Taskid = %s;'
                        cursor.execute(insert_last_triggered, (date_time,taskid))
                        DBConn.commit()
                        log(f'Last triggered updated to {date_time} On TaskId {taskid}.')  

                elif schedule_type == 'interval' and trigger_time:
                    print('Schedule type is Interval!')
                    interval = int(schedule['interval'])

                    if last_triggered is not None:
                        next_trigger_day = last_triggered.date() + datetime.timedelta(days=interval)
                    else:
                        next_trigger_day = created_at.date() + datetime.timedelta(days=interval)

                    next_trigger = datetime.datetime.combine(next_trigger_day, trigger_dt)

                    print(f'Försöka få ihop datum och tid {next_trigger_day} {trigger_time}')
                    print(f'Trigger time: {next_trigger}. Now time: {date_time}')


                    if (next_trigger <= date_time) and (last_triggered is None or last_triggered.date() < today):
                    #if trigger_dt <= date_time and last_triggered is None:
                        print('Trigger hit!!')

                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')

                        insert_last_triggered = 'UPDATE Tasks SET Lasttriggered = %s WHERE Taskid = %s;'
                        cursor.execute(insert_last_triggered, (date_time,taskid))
                        DBConn.commit()
                        log(f'Last triggered updated to {date_time} On TaskId {taskid}.')              

    start_time, finish_time, operation_time = performance.timed_operation(Schedulerjob)
    print(f'{colors.WARNING}')
    print('Performance monitor!')
    print(f'Start time: {start_time.strftime("%H:%M:%S")}. Finish time: {finish_time.strftime("%H:%M:%S")}')
    print(f'Operation time: {operation_time:.2f} seconds.')
    print(f'{colors.ENDC}')               


if __name__ == '__main__':
    event_trigger()