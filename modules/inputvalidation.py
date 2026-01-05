from modules.logger import log,debug,info,warning,error,critical
import re
import datetime

debug = False

def inputvalidation(fields:dict) -> bool:
    if debug: print('Starting input validation')

    validate = True
    message = []
    issue = []

    for fields,container in fields.items():
        type=container.get('type')
        required=container.get('required')
        value_raw=container.get('value')
        value=str(container.get('value'))

        if debug:
            print(f'Input: {value}')
            print(f'Container: {container}')
            print(f'Type: {type}')
            print(f'Required: {required}.')

        if not required and (value_raw is None or value.strip() == ''):
            continue


        if type == 'text':
            if len(value.strip()) > 0 and len(value.strip()) < 3000:
                message.append('Approved text input!')
            else: 
                validate = False
                issue.append(f'Invalid text input detected in: {value}!')

        elif type == 'email':
            if re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', value):
                message.append('Approved email!')
            else: 
                validate = False
                issue.append(f'Invalid email detected in {value}!')

        elif type == 'phone':
            if re.match(r'^\+?\d{7,15}$', value):
                message.append('Approved phone number!')
            else: 
                validate = False
                issue.append(f'Invalid phone number detected in: {value}!')

        elif type == 'http':
            if re.match(r'^https?://', value):
                message.append('Approved http!')
            else: 
                validate = False
                issue.append(f'Invalid http detected in: {value}!')

        elif type == 'integer':
            if re.match(r'^\d+$', value):
                message.append('Approved integer!')
            else: 
                validate = False
                issue.append(f'Invalid integer detected in {value}!')

        elif type == 'monthlydate':
            if int(value) > 0 and int(value) <= 31:
                message.append('Approved monthly date!')
            else: 
                validate = False
                issue.append(f'Invalid monthly date detected in {value}!')

        elif type == 'datetime':
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
                message.append('Approved datetime!')
            except ValueError: 
                validate = False
                issue.append(f'Invalid datetime detected in {value}!')

        elif type == 'time':
            try: 
                datetime.datetime.strptime(value, "%H:%M")
                message.append('Approved time!')
            except ValueError as err: 
                validate = False
                issue.append(f'Invalid time detected in {value}!')

        elif type == 'days':
            days = ['mon','tue','wed','thu','fri','sat','sun']
            splitvalue = [d.strip().lower() for d in value.split(',')]

            for d in splitvalue:
                if d in days:
                    message.append(f'Approved day {d}!')
                else: 
                    validate = False
                    issue.append(f'Invalid day detected in {d}!')
            

        else:
            validate = False

    if debug:
        print('Input validation result (debug mode):')
        for mess in message:
            print(f'- {mess}')

    if issue:
        print('Following issue(s) is returned from the input validation: ')
        for err in issue:
            print(f'- {err}')

    return validate

