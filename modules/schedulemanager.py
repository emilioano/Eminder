import json
import datetime

from modules.logger import log,debug,info,warning,error,critical
from config import DBCONFIG,colors
from output import mail_out, discord_out, reports
from analysis import performance

from modules import dbactions


class TaskManager:
    def __init__(self):
        self.date_time = datetime.datetime.now()
        self.today = self.date_time.date()
        self.year = self.date_time.year

    def fetch_tasks(self):
        return dbactions.fetchtasks()

    def messageout(self, channel, recipient_email, mail_subject, task_message, recipient_discordhook=None):
        if channel == 1:
            mail_out.gmail_send_message(recipient_email,mail_subject,task_message) 
        elif channel == 2:
            discord_out.discord_send_message(recipient_discordhook, mail_subject + '. ' + task_message)
        elif channel == 3:
            mail_out.gmail_send_message(recipient_email,mail_subject,task_message)
            discord_out.discord_send_message(recipient_discordhook, mail_subject + '. ' + task_message)

    def task_handler(self, row):
        # DB fields to read
        schedule_raw = row.get('Schedule')
        schedule = json.loads(schedule_raw)
        schedule_type = schedule['type']
        last_triggered = row.get('Lasttriggered') 
        created_at = row.get('Createdtime')
        trigger_time = schedule['time']
        channel = row.get('Channel')

        # Mail/output builder
        recipient_id = row.get('RecipientId')
        recipient_name = row.get('Name')
        recipient_email = row.get('Email')
        recipient_phone = row.get('Phone')
        recipient_discordhook = row.get('DiscordHook')

        mail_subject = row.get('Subject') 
        if mail_subject is None:
            mail_subject = f'Alert from Eminder to {recipient_name}!'
        
        task_message = row.get('Message') + ' \n[ This is an alert from Eminder triggered at ' + schedule_type + ' ' + trigger_time + '. Recipient: ' + recipient_name + ' ] '
    
        # Different datetime format for trigger depending on schedule type
        if schedule_type == 'once' or schedule_type == 'yearly':
            trigger_dt = datetime.datetime.strptime(trigger_time, "%Y-%m-%d %H:%M")
        else:
            trigger_dt = datetime.datetime.strptime(trigger_time, "%H:%M").time()


        # Printing some task details to the screen which can be nice for debugging.
        taskid = row.get('TaskId')
        print('='*60)
        print(f'Taskid: {taskid}')
        print(f'RecipientId: {recipient_id}. Recipient name: {recipient_name}. Recipient e-mail: {recipient_email}. Recipient_phone: {recipient_phone}. Channel: {channel}. Discord Hook: {recipient_discordhook}')
        if mail_subject is not None:
            print(f'Subject: {mail_subject}')
        print(f'Message: {task_message}')

        # Detecting task triggers
        if schedule_type == 'once' and trigger_time:
            print('Schedule type is Once!')
            print(f'Trigger time: {trigger_dt}. Now time: {self.date_time}')
            if trigger_dt <= self.date_time and last_triggered is None:
                print('Trigger hit!!')
                self.execute(row, channel, mail_subject, task_message)

        elif schedule_type == 'daily' and trigger_time:
            print('Schedule type is Daily!')
            print(f'Trigger time: {trigger_dt}. Now time: {self.date_time}')
            if (trigger_dt <= self.date_time.time()) and (last_triggered is None or last_triggered.date() < self.today):
                print('Trigger hit!!')
                self.execute(row, channel, mail_subject, task_message)

        elif schedule_type == 'monthly' and trigger_time:
            print('Schedule type is Monthly!')
            trigger_days = int(schedule['days'])
            current_weekday = int(datetime.datetime.now().day)  

            print(f'Today in numbers: {current_weekday}')
            print(f'Trigger time: {trigger_dt}. Now time: {self.date_time}')
            print(f'Trigger-dagar: {trigger_days}')

            if (current_weekday == trigger_days) and (trigger_dt <= self.date_time.time()) and (last_triggered is None or last_triggered.date() < self.today):
                print('Trigger hit!!')
                self.execute(row, channel, mail_subject, task_message)

        elif schedule_type == 'weekly' and trigger_time:
            print('Schedule type is Weekly!')
            trigger_days = schedule['days']
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

            print(f'Today with three letters: {day}')
            print(f'Trigger time: {trigger_dt}. Now time: {self.date_time}')
            print(f'Trigger days: {trigger_days}')

            if (day in trigger_days) and (trigger_dt <= self.date_time.time()) and (last_triggered is None or last_triggered.date() < self.today):
                print('Trigger hit!!')
                self.execute(row, channel, mail_subject, task_message)

        elif schedule_type == 'interval' and trigger_time:
            print('Schedule type is Interval!')
            interval = int(schedule['interval'])

            if last_triggered is not None:
                next_trigger_day = last_triggered.date() + datetime.timedelta(days=interval)
            else:
                next_trigger_day = created_at.date() + datetime.timedelta(days=interval)

            next_trigger = datetime.datetime.combine(next_trigger_day, trigger_dt)

            print(f'Trying to put together date and time: {next_trigger_day} {trigger_time}')
            print(f'Trigger time: {next_trigger}. Now time: {self.date_time}')


            if (next_trigger <= self.date_time) and (last_triggered is None or last_triggered.date() < self.today):
                print('Trigger hit!!')
                self.execute(row, channel, mail_subject, task_message)

        elif schedule_type == 'yearly' and trigger_time:
            print('Schedule type is Yearly!')

            # Set dummy year
            trigger_no_year = trigger_dt.replace(year=9999)
            now_no_year = self.date_time.replace(year=9999)

            print(f'Trigger time: {trigger_no_year}. Now time: {now_no_year}')

            if (trigger_no_year <= now_no_year) and (last_triggered is None or last_triggered.year <= self.year-1):
                print('Trigger hit!!')  
                self.execute(row, channel, mail_subject, task_message)

    def execute(self, row, channel, subject, message):
        recipient_email = row.get('Email')
        recipient_discordhook = row.get('DiscordHook')

        try:
            start_time, finish_time, operation_time = performance.timed_operation(self.messageout, channel, recipient_email, subject, message, recipient_discordhook)
            log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')

            dbactions.setlasttriggered(self.date_time, row.get('TaskId'))
        except Exception as err:
            error(f'{err}') 

    def run(self):
        def schedulerjob():
            for row in self.fetch_tasks():
                if row.get('Active') == 1:
                    self.task_handler(row)

        start_time, finish_time, operation_time = performance.timed_operation(schedulerjob)
        print(f'{colors.WARNING}')
        print('Performance monitor!')
        print(f'Start time: {start_time.strftime("%H:%M:%S")}. Finish time: {finish_time.strftime("%H:%M:%S")}')
        print(f'Operation time: {operation_time:.2f} seconds.')
        print(f'{colors.ENDC}')               

        performance.timed_operation(reports.dailyreportjob)












### Below is the function before refactoring into class, keeping it as a memory for now ###
def event_trigger():

    def Schedulerjob():
        row = dbactions.fetchtasks()  

        date_time = datetime.datetime.now()
        today = datetime.datetime.now().date()

        # Looping through the tasks
        for row in row:

            def Messageout():
                # Send to message_out!!
                if channel == 1:
                    mail_out.gmail_send_message(recipient_email,mail_subject,task_message) 
                elif channel == 2:
                    discord_out.discord_send_message(recipient_discordhook, mail_subject + '. ' + task_message)
                elif channel == 3:
                    mail_out.gmail_send_message(recipient_email,mail_subject,task_message)
                    discord_out.discord_send_message(recipient_discordhook, mail_subject + '. ' + task_message)


            if (row.get('Active')) == 1:

                # Fetching fields from DB records
                schedule_raw = row.get('Schedule')
                schedule = json.loads(schedule_raw)

                schedule_type = schedule['type']
                last_triggered = row.get('Lasttriggered') 
                created_at = row.get('Createdtime')
                trigger_time = schedule['time']
                channel = row.get('Channel')

                recipient_id = row.get('RecipientId')
                recipient_name = row.get('Name')
                recipient_email = row.get('Email')
                recipient_phone = row.get('Phone')
                recipient_discordhook = row.get('DiscordHook')

                task_message = row.get('Message') + ' \n[ This is an alert from Eminder triggered at ' + schedule_type + ' ' + trigger_time + '. Recipient: ' + recipient_name + ' ] '

                
                mail_subject = row.get('Subject') 
                if mail_subject is None:
                    mail_subject = f'Alert from Eminder to {recipient_name}!'

                # Different datetime format for trigger depending on schedule type
                if schedule_type == 'once':
                    trigger_dt = datetime.datetime.strptime(trigger_time, "%Y-%m-%d %H:%M") 
                else:
                    trigger_dt = datetime.datetime.strptime(trigger_time, "%H:%M").time()


                taskid = row.get('TaskId')

                print('='*60)
                print(f'Taskid: {taskid}')
                print(f'RecipientId: {recipient_id}. Recipient name: {recipient_name}. Recipient e-mail: {recipient_email}. Recipient_phone: {recipient_phone}. Channel: {channel}')
                if mail_subject is not None:
                    print(f'Subject: {mail_subject}')
                print(f'Message: {task_message}')

                

                # Apply different calculation logic depending on the Schedule Type
                if schedule_type == 'once' and trigger_time:
                    print('Schedule type is Once!')

                    print(f'Trigger time: {trigger_dt}. Now time: {date_time}')
                    if trigger_dt <= date_time and last_triggered is None:
                        print('Trigger hit!!')

                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')

                        # Updating last triggered datetime on task
                        dbactions.setlasttriggered(date_time,taskid)

                elif schedule_type == 'daily' and trigger_time:
                    print('Schedule type is Daily!')
                    print(f'Trigger time: {trigger_dt}. Now time: {date_time}')
                    if (trigger_dt <= date_time.time()) and (last_triggered is None or last_triggered.date() < today):

                        print('Trigger hit!!')
                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')

                        # Updating last triggered datetime on task
                        dbactions.setlasttriggered(date_time,taskid)

                elif schedule_type == 'monthly' and trigger_time:
                    print('Schedule type is Monthly!')

                    trigger_days = int(schedule['days'])
                    current_weekday = int(datetime.datetime.now().day)  

                    print(f'IToday in numbers: {current_weekday}')
                    print(f'Trigger time: {trigger_dt}. Now time: {date_time}')
                    print(f'Trigger-dagar: {trigger_days}')

                    if (current_weekday == trigger_days) and (trigger_dt <= date_time.time()) and (last_triggered is None or last_triggered.date() < today):
                        print('Trigger hit!!')

                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')

                        # Updating last triggered datetime on task
                        dbactions.setlasttriggered(date_time,taskid)


                elif schedule_type == 'weekly' and trigger_time:
                    print('Schedule type is Weekly!')

                    trigger_days = schedule['days']
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

                    print(f'Today with three letters: {day}')
                    print(f'Trigger time: {trigger_dt}. Now time: {date_time}')
                    print(f'Trigger-dagar: {trigger_days}')

                    if (day in trigger_days) and (trigger_dt <= date_time.time()) and (last_triggered is None or last_triggered.date() < today):
                        print('Trigger hit!!')

                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')

                        # Updating last triggered datetime on task
                        dbactions.setlasttriggered(date_time,taskid)


                elif schedule_type == 'interval' and trigger_time:
                    print('Schedule type is Interval!')
                    interval = int(schedule['interval'])

                    if last_triggered is not None:
                        next_trigger_day = last_triggered.date() + datetime.timedelta(days=interval)
                    else:
                        next_trigger_day = created_at.date() + datetime.timedelta(days=interval)

                    next_trigger = datetime.datetime.combine(next_trigger_day, trigger_dt)

                    print(f'Trying to put together date and time: {next_trigger_day} {trigger_time}')
                    print(f'Trigger time: {next_trigger}. Now time: {date_time}')


                    if (next_trigger <= date_time) and (last_triggered is None or last_triggered.date() < today):
                        print('Trigger hit!!')

                        # Sending message and monitoring the operation time!
                        start_time, finish_time, operation_time = performance.timed_operation(Messageout)
                        log(f'Operation time: {operation_time:.2f}s. Start time: {start_time}. Finish time {finish_time}.')

                        # Updating last triggered datetime on task
                        dbactions.setlasttriggered(date_time,taskid)
  
    start_time, finish_time, operation_time = performance.timed_operation(Schedulerjob)

    performance.timed_operation(reports.DailyReportJob)

    print(f'{colors.WARNING}')
    print('Performance monitor!')
    print(f'Start time: {start_time.strftime("%H:%M:%S")}. Finish time: {finish_time.strftime("%H:%M:%S")}')
    print(f'Operation time: {operation_time:.2f} seconds.')
    print(f'{colors.ENDC}')   

              



#if __name__ == '__main__':
#    event_trigger()

if __name__ == '__main__':        
    TaskManager().run()