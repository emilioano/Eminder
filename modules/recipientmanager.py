import mysql.connector
from config import DBCONFIG
from modules.logger import log,debug,info,warning,error,critical

DBConn = mysql.connector.connect(**DBCONFIG);
cursor = DBConn.cursor()

def run_recipient_program(TaskId=None):
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

        for row in result:
            log(row)


    if selection == 2:
        print('Enter the required input fields')

        name = str(input('Name: '))
        email = str(input('Email: '))
        phone = str(input('Phone # (optional): '))
        discord_webhhok = str(input('Discord Webhook (optional): '))

        sql = 'INSERT INTO Recipients(Name,Email,Phone,DiscordHook) VALUES (%s,%s,%s,%s);'




        try:
            cursor.execute(sql, (name,email,phone))
            saved_id = cursor.lastrowid
            DBConn.commit()
            

            if TaskId:
                sql2 = 'INSERT INTO TaskRecipients(Taskid,RecipientId) VALUES (%s,%s);'
                cursor.execute(sql2, (TaskId,saved_id))
                DBConn.commit()


        except Exception as err:
            print(err)


    if selection == 3:
        print('Enter the id for the record to remove')

        id = str(input('Id: '))

        sql = 'DELETE FROM Recipients Where Id = %s;'

        try:
            cursor.execute(sql, (id))
            DBConn.commit()
        except Exception as err:
            (print(err))

        




if __name__ == '__main__':
    run_recipient_program()