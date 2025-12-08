import mysql.connector

EmilsSchedulerDB = mysql.connector.connect(host='localhost',user='root',password='0popcorn0',database='EmilsSchedulerDB');
cursor = EmilsSchedulerDB.cursor()

def run_recipient_program():
    print('='*60)
    print('Make a selection.')
    print('1. View records in DB.')
    print('2. Enter a new record into DB')
    print('3. Remove a record from DB')
    selection = int(input())
    print('='*60)


    if selection == 1:
        print('Showing records')
        cursor.execute('SELECT * FROM Recipients')

        result = cursor.fetchall()

        print (result)


    if selection == 2:
        print('Enter the required input fields')

        name = str(input('Name: '))
        email = str(input('Email: '))
        phone = str(input('Phone #: '))

        sql = 'INSERT INTO Recipients(Name,Email,Phone) VALUES (%s,%s,%s);'

        try:
            cursor.execute(sql, (name,email,phone))
            EmilsSchedulerDB.commit()
        except Exception as err:
            print(err)


    if selection == 3:
        print('Enter the id for the record to remove')

        id = str(input('Id: '))

        sql = 'DELETE FROM Recipients Where Id = %s;'

        try:
            cursor.execute(sql, (id))
            EmilsSchedulerDB.commit()
        except Exception as err:
            (print(err))

        





run_recipient_program()