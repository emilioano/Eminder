import mysql.connector
import json
import datetime
from modules.logger import log,debug,info,warning,error,critical
from modules import recipientmanager

from config import DBCONFIG



DBConn = mysql.connector.connect(**DBCONFIG);
cursor = DBConn.cursor()


def run_task_manager():

    selection = 0

    saved_id = None

    while selection < 999:
        if selection == 0:
            print('='*60)
            print('Make a selection.')
            print('1. View records in DB.')
            print('2. Enter a new record into DB')
            print('3. Remove a record from DB')
            print('4. Connect an existing recipient to a task.')
            print('0. Quit')
            selection = int(input())
            print('='*60)


        if selection == 1:
            
            try:
                cursor.execute('SELECT * FROM Tasks ORDER By TaskId ASC')
                result = cursor.fetchall()

                log('Listing records in Task table:')
                for row in result:
                    log(row)
                    #print(result)

                return

            except Exception as err:
                print(err)

                return


        if selection == 2:

            schedule = {}

            print('Enter the required input fields: ')

            print('Choose schedule: ')
            print(' 1. Once \n 2. Daily \n 3. Weekly \n 4. Monthly \n 5. Interval')
            scheduleinput = int(input('When to send message: '))

            if scheduleinput == 1:
                dateandtime = input('Enter date and time YYYY-MM-DD HH:MM: ')

                schedule = {
                    'type': 'once',
                    'time': dateandtime,
                    'timezone': 'CET'
                }

            elif scheduleinput == 2:
                time = input('Enter which time the send message, HH:MM: ')      

                schedule = {
                    'type': 'daily' , 
                    'time': time,
                    'timezone': 'CET'
                }    

            elif scheduleinput == 3:
                days = input('Enter which days to send message. Format: mon, tue, wed, thu, fri: ')
                time = input('Enter the time to send message, HH:MM: ')

                schedule = {
                    'type': 'weekly',
                    'days': days,
                    'time': time,
                    'timezone': 'CET'
                }            

            elif scheduleinput == 4:
                days = input ('Enter which dates of the month to send message, (example: 15, 29): ')
                time = input('Enter the time to send message, HH:MM: ')

                schedule = {
                    'type': 'monthly',
                    'days': days,
                    'time': time,
                    'timezone': 'CET'
                }   

            elif scheduleinput == 5:
                interval = input('Enter which interval to send message (example for every third day: 3): ')
                time = input('Enter which time the send message, HH:MM: ') 

                schedule = {
                    'type': 'interval',
                    'interval': interval,
                    'time': time,
                    'timezone': 'CET'
                }   


            channel = int(input('Channels to use (1. E-mail. 2. Text message. 3. All): '))
            dailyquote = str(input('Include a daily quote (Y/N): '))
            dailyquote = 1 if dailyquote == 'Y' else 0
            dailyweather = str(input('Include the daily weather (Y/N): '))
            dailyweather = 1 if dailyweather == 'Y' else 0
            #if dailyweather == 'Y':
            location = input('Enter weather location: ') if dailyweather == 1 else 0

            message = str(input('The message to be sent (max 3000 characters):'))

            


            now_str = str(datetime.datetime.now())
            date_time = (now_str.split('.')[0])

            sql = 'INSERT INTO Tasks(Message,Dailyquote,Dailyweather,Schedule,Channel,Location,Createdtime) VALUES (%s,%s,%s,%s,%s,%s,%s);'



            try:
                cursor.execute(sql, (message,dailyquote,dailyweather,json.dumps(schedule),channel,location,date_time))
                DBConn.commit()
                saved_id = cursor.lastrowid
                log(f'TaskId {saved_id} has been saved! Message: {message}. Schedule: {json.dumps(schedule)}.')

                recipient_question = str(input('Recipients (1. Add new. 2. Add recipient from existing): '))
                if recipient_question == str(1):
                    recipientmanager.run_recipient_program(saved_id)
                if recipient_question == str(2):
                    selection = 4
                
                continue

            except Exception as err:
                error(err)

                return

        if selection == 3:
            print('Enter the Taskid for the record to remove')

            taskid = input('Taskid: ')

            sql = 'DELETE FROM Tasks Where Taskid = %s;'

            try:
                cursor.execute(sql, (taskid,))
                DBConn.commit()
                log(f'Removed Taskid {taskid} from DB.')
                return

            except Exception as err:
                error(err)
                return


        if selection == 4:

            sql = 'INSERT INTO TaskRecipients(TaskId,RecipientId) VALUES (%s,%s);'

            print('1. Show all saved recipients. 2. Enter Id')
            question = str(input(''))

            if question == str(1):
                cursor.execute('SELECT * FROM Recipients')

                log('Listing all recipients:')
                result = cursor.fetchall()

                for row in result:
                    log(row)
            
            if saved_id:
                recipient_id = input(f'Enter the RecipientId to connect to TaskId {saved_id}.')
            
            else:
                saved_id = input('Enter the TaskId.')
                recipient_id = input(f'Enter the RecipientId to connect to TaskId {saved_id}.')

            try:
                cursor.execute(sql, (saved_id,recipient_id))
                DBConn.commit()
                log(f'TaskId {saved_id} has been connected to RecipientId {recipient_id}.')
                return
            except Exception as err:
                error(err)
                return

                


        selection = 1000 if selection == 0 else 1



if __name__ == '__main__':
    run_task_manager()