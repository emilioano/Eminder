
import json
import datetime
from eminder.utils import log,debug,info,warning,error,critical
from eminder.services import recipientmanager
from eminder.db import dbactions
from eminder.validation import inputvalidation
from eminder.integrations import AIprompt

def menuoptions():
                print('='*60)
                print('Make a selection.')
                print('1. View records in DB.')
                print('2. Enter a new record into DB')
                print('3. Use AI to make a schedule.')
                print('4. Remove a record from DB')
                print('5. Connect an existing recipient to a task.')
                print('0. Quit')
                print('='*60)

def run_task_manager():
    selection = 0

    saved_id = None

    while True:
        try:
            menuoptions()
            selection = int(input())
            saved_posts = []

            if selection < 0 or selection > 5:
                print('='*60)
                print('Invalid selection, try again!')
                print('='*60)
                continue


            elif selection == 1:
                try:
                    dbactions.viewtasks()
                except Exception as err:
                    error(err)

            elif selection == 2:
                dateandtime, time, days, interval, monthlydate = None, None, None, None, None
                timereq = True
                datetimereq = False

                schedule = {}

                print('Enter the required input fields: ')

                print('Choose schedule: ')
                print(' 1. Once \n 2. Daily \n 3. Weekly \n 4. Monthly \n 5. Interval \n 6. Yearly')
                scheduleinput = int(input('When to send message: '))

                if scheduleinput < 0 or scheduleinput > 6:
                    print('='*60)
                    print('Invalid selection, try again!')
                    print('='*60)
                    continue

                elif scheduleinput == 1:
                    dateandtime = input('Enter date and time YYYY-MM-DD HH:MM: ')
                    datetimereq = True
                    timereq = False

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
                    days = input('Enter which days to send message. Format: mon, tue, wed, thu, fri: ').strip().replace(' ','')
                    time = input('Enter the time to send message, HH:MM: ')

                    schedule = {
                        'type': 'weekly',
                        'days': days,
                        'time': time,
                        'timezone': 'CET'
                    }            

                elif scheduleinput == 4:
                    monthlydate = input ('Enter which dates of the month to send message, (example: 15, 29): ')
                    time = input('Enter the time to send message, HH:MM: ')

                    schedule = {
                        'type': 'monthly',
                        'days': monthlydate,
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

                elif scheduleinput == 6:
                    dateandtime = input('Enter date and time for the first occurance YYYY-MM-DD HH:MM: ')
                    datetimereq = True
                    timereq = False

                    schedule = {
                        'type': 'yearly',
                        'time': dateandtime,
                        'timezone': 'CET'
                    }


                channel = int(input('Channels to use (1. E-mail. 2. Discord bot. 3. All): '))
                if channel < 0 or channel > 3:
                    print('='*60)
                    print('Invalid selection, try again!')
                    print('='*60)
                    continue

                ### Below is functionality to build in the future, not included in MVP version ###

                #dailyquote = str(input('Include a daily quote (Y/N): '))
                #dailyquote = 1 if dailyquote == 'Y' else 0
                #dailyweather = str(input('Include the daily weather (Y/N): '))
                #dailyweather = 1 if dailyweather == 'Y' else 0
                #if dailyweather == 'Y':
                #location = input('Enter weather location: ') if dailyweather == 1 else 0

                subject = str(input('Enter a subject for the message: '))
                message = str(input('The message to be sent:'))

                now_str = str(datetime.datetime.now())
                date_time = (now_str.split('.')[0])

                # Fields to input validate
                val_fields = {
                    'scheduleinput':{'value':scheduleinput,'type':'integer','required':True},
                    'dateandtime':{'value':dateandtime,'type':'datetime','required':datetimereq},
                    'time':{'value':time,'type':'time','required':timereq},
                    'days':{'value':days,'type':'days','required':False},
                    'monthlydate':{'value':monthlydate,'type':'monthlydate','required':False},
                    'interval':{'value':interval,'type':'integer','required':False},
                    'channel':{'value':channel,'type':'integer','required':True},
                    'subject':{'value':subject,'type':'text','required':True},
                    'message':{'value':message,'type':'text','required':True}
                }

                validate = inputvalidation(val_fields)
                if not validate:
                    print('Invalid input in field(s) detected, please try again!')
                    selection = 2
                    continue

                elif validate:
                    try:
                        saved_id = dbactions.inserttask(subject,message,'0','0',json.dumps(schedule),channel,'',date_time)
                        print(saved_id)
                    except Exception as err:
                        error(err)

                recipient_question = str(input('Recipients (1. Add new. 2. Add recipient from existing): '))
                if recipient_question == str(1):
                    recipientmanager.run_recipient_program(saved_id)
                if recipient_question == str(2):
                    selection = 5

            elif selection == 3:
                print("Describe what you want to schedualize!")
                prompt = input()
                val_fields = {'prompt':{'value':prompt,'type':'text','required':True},}
                validate = inputvalidation(val_fields)

                if not validate:
                    print('Invalid input in field(s) detected, please try again!')
                    selection = 2
                    continue
                elif validate:


                    airesponse_regex = AIprompt(prompt)
                    jsonresponse = json.loads(airesponse_regex)
                    answers = jsonresponse["answers"]
    
                    savepost = input('Do you want to save this record(s)? Y/N')
    
                    if savepost == "Y":
                        channel = int(input('Channels to use (1. E-mail. 2. Discord bot. 3. All): '))
    
                        now_str = str(datetime.datetime.now())
                        date_time = (now_str.split('.')[0])
    
                        # Fields to input validate
                        val_fields = {
                            'channel':{'value':channel,'type':'integer','required':True},
                        }
    
                        validate = inputvalidation(val_fields)
                        if not validate:
                            print('Invalid input in field(s) detected, please try again!')
                            selection = 2
                            continue
                        
                        elif validate:
                            for answer in answers:
                                subject = answer["Subject"]
                                text = answer["Message"]
                                schedule = answer["schedule"]
    
                                try:
                                    saved_id = dbactions.inserttask(subject,text,'0','0',json.dumps(schedule),channel,'',date_time)
                                    print(saved_id)
                                    saved_posts.append(saved_id)
                                except Exception as err:
                                    error(err)
    
                        recipient_question = str(input('Recipients (1. Add new. 2. Add recipient from existing): '))
                        if recipient_question == str(1):
                            recipientmanager.run_recipient_program(i)
                        if recipient_question == str(2):
                            selection = 5
    
                    else:
                        selection = 3


            elif selection == 4:
                print('Enter the Taskid for the record to remove')

                taskid = int(input('Taskid: '))

                 # Fields to validate input, input:type
                val_fields = { 'taskid':{'value':taskid,'type':'integer','required':True}}

                validate = inputvalidation(val_fields)

                if not validate:
                    print('Invalid input in field(s) detected, please try again!')
                    selection = 3
                    continue

                elif validate:
                    try:
                        dbactions.deletetask(taskid)
                    except Exception as Err:
                        error(Err)


            if selection == 5:
                print('1. Show all saved recipients. 2. Enter Id')
                question = str(input(''))

                if question == str(1):
                    try:
                        dbactions.viewrecipients()
                    except Exception as err:
                        error(err)

                if saved_id:
                    recipient_id = input(f'Enter the RecipientId to connect to TaskId {saved_id}.')

                else:
                    saved_id = input('Enter the TaskId.')
                    recipient_id = input(f'Enter the RecipientId to connect to TaskId {saved_id}.')


                 # Fields to validate input, input:type
                val_fields = {
                    'question':{'value':question,'type':'integer','required':True},
                    'recipient_id':{'value':recipient_id,'type':'integer','required':True},
                    'saved_id':{'value':saved_id,'type':'integer','required':True}
                    }

                validate = inputvalidation.inputvalidation(val_fields)

                if not validate:
                    print('Invalid input in field(s) detected, please try again!')
                    selection = 3
                    continue

                elif validate:
                    try:
                        if saved_posts:
                            for i in saved_posts:
                                dbactions.createconnection(i,recipient_id)
                        else:
                            dbactions.createconnection(saved_id,recipient_id)
                            return
                    except Exception as Err:
                        error(Err)
                        
                

            elif selection == 0:
                break


        except ValueError:
            print('='*60)
            print('Invalid selection, try again!')
            print('='*60)
            continue


if __name__ == '__main__':
    run_task_manager()