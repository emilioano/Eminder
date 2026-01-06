from eminder.utils import log,debug,info,warning,error,critical
from eminder.db import dbactions
from eminder.validation import inputvalidation

def menuoptions():
    print('='*60)
    print('Make a selection.')
    print('1. View records in DB.')
    print('2. Enter a new record into DB')
    print('3. Remove a record from DB')
    print('0. Exit')
    print('='*60)


def run_recipient_program(TaskId=None):
    if TaskId:
        selection = 2
    else:
        selection = 0

    validate = False

    while True:
        try:
            menuoptions()
            selection = int(input())

            if selection < 0 or selection > 3:
                print('='*60)
                print('Invalid selection, try again!')
                print('='*60)
                continue

            elif selection == 1:
                print('Showing records')
                
                try:
                    dbactions.viewrecipients()
                except Exception as err:
                    error(err)

            elif selection == 2:
                print('Enter the required input fields')

                name = str(input('Name: '))
                email = str(input('Email: '))
                phone = str(input('Phone # (optional): '))
                discord_webhook = str(input('Discord Webhook (optional): '))

                # Fields to input validate
                val_fields = {
                    'name':{'value':name,'type':'text','required':True},
                    'email':{'value':email,'type':'email','required':True},
                    'phone':{'value':phone,'type':'phone','required':False},
                    'discord_webhook':{'value':discord_webhook,'type':'http','required':False}
                }

                validate = inputvalidation(val_fields)

                if not validate:
                    print('Invalid input in field(s) detected, please try again!')
                    selection = 2
                    continue

                elif validate:
                    try:
                        dbactions.insertrecipient(name,email,phone,discord_webhook,TaskId)
                        if TaskId:
                            break
                    except Exception as Err:
                        error(Err)

                

            elif selection == 3:
                print('Enter the id for the record to remove')

                id = str(input('Id: '))

                # Fields to validate input, input:type
                val_fields = { 'id':{'value':id,'type':'integer','required':True}}

                validate = inputvalidation(val_fields)

                if not validate:
                    print('Invalid input in field(s) detected, please try again!')
                    selection = 3
                    continue

                elif validate:
                    try:
                        dbactions.deleterecipient(id)
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
    run_recipient_program()