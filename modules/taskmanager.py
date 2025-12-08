import mysql.connector
import json
import datetime
from emilflow.modules import log

EmilsSchedulerDB = mysql.connector.connect(host='localhost',user='root',password='0popcorn0',database='EmilsSchedulerDB');
cursor = EmilsSchedulerDB.cursor()



def run_recipient_program():

    selection = 0

    while selection < 999:
        if selection == 0:
            print('='*60)
            print('Make a selection.')
            print('1. View records in DB.')
            print('2. Enter a new record into DB')
            print('3. Remove a record from DB')
            print('0. Quit')
            selection = int(input())
            print('='*60)


        if selection == 1:
            print('Showing records')
            
            try:
                cursor.execute('SELECT * FROM Tasks')
                result = cursor.fetchall()

                log(result)
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
                    'timezone': 'Europe/Stockholm'
                }

            elif scheduleinput == 2:
                time = input('Enter which time the send message, HH:MM: ')      

                schedule = {
                    'type': 'daily' , 
                    'time': time,
                    'timezone': 'Europe/Stockholm'
                }    

            elif scheduleinput == 3:
                days = input('Enter which days to send message. Format: mon, tue, wed, thu, fri: ')
                time = input('Enter the time to send message, HH:MM: ')

                schedule = {
                    'type': 'weekly',
                    'days': days,
                    'time': time,
                    'timezone': 'Europe/Stockholm'
                }            

            elif scheduleinput == 4:
                days = input ('Enter which dates of the month to send message, (example: 15, 29): ')
                time = input('Enter the time to send message, HH:MM: ')

                schedule = {
                    'type': 'monthly',
                    'days': days,
                    'time': time,
                    'timezone': 'Europe/Stockholm'
                }   

            elif scheduleinput == 5:
                interval = input('Enter which interval to send message (example for every third day: 3): ')
                time = input('Enter which time the send message, HH:MM: ') 

                schedule = {
                    'type': 'interval',
                    'interval': interval,
                    'time': time,
                    'timezone': 'Europe/Stockholm'
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
                EmilsSchedulerDB.commit()
                print('Post saved!')

                return

            except Exception as err:
                print(err)

                return

        if selection == 3:
            print('Enter the Taskid for the record to remove')

            taskid = input('Taskid: ')

            sql = 'DELETE FROM Tasks Where Taskid = %s;'

            try:
                cursor.execute(sql, (taskid,))
                EmilsSchedulerDB.commit()
                return

            except Exception as err:
                (print(err))
                return


        selection = 1000 if selection == 0 else 1




run_recipient_program()