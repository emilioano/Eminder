import mysql.connector
from config import DBCONFIG
from modules.logger import log,debug,info,warning,error,critical

DBConn = mysql.connector.connect(**DBCONFIG);
cursor = DBConn.cursor()
cursor_dict = DBConn.cursor(dictionary=True)


### RECIPIENT MANAGER DB ACTIONS ###
def viewrecipients():
    cursor.execute('SELECT * FROM Recipients')
    result = cursor.fetchall()

    try:
        for row in result:
            print(row)
    except Exception as err:
        error(err)    



def insertrecipient(name,email,phone=None,discord_webhook=None,TaskId=None):
    sql = 'INSERT INTO Recipients(Name,Email,Phone,DiscordHook) VALUES (%s,%s,%s,%s);'

    try:
        cursor.execute(sql, (name,email,phone,discord_webhook))
        saved_id = cursor.lastrowid
        DBConn.commit()
        log(f'New record was inserted into the Recipients table with Id: {saved_id}, name: {name}, email: {email}.')
        
        if TaskId:
            sql = 'INSERT INTO TaskRecipients(Taskid,RecipientId) VALUES (%s,%s);'
            cursor.execute(sql, (TaskId,saved_id))
            DBConn.commit()
            log(f'TaskId {saved_id} has been connected with Recipient {name}, {email}.')

    except Exception as err:
        DBConn.rollback()
        error(err)

def deleterecipient(id):
    sql = 'DELETE FROM Recipients Where RecipientId = %s'

    try:
        cursor.execute(sql, (id,))
        DBConn.commit()
        log(f'Record with id {id} was deleted from the Recipients table!')
    except Exception as err:
        DBConn.rollback()
        error(err)
### END RECIPIENT MANAGER DB ACTIONS ###


### TASK MANAGER DB ACTIONS ###
def viewtasks():
    try:
        cursor.execute('SELECT * FROM Tasks WHERE Active = "1" ORDER By TaskId ASC;')
        result = cursor.fetchall()

        print('Listing records in Task table:')
        for row in result:
            print(f'{row}\n')

    except Exception as err:
        error(err)

def inserttask(subject,message,dailyquote,dailyweather,schedule,channel,location,date_time) -> int:
    sql = 'INSERT INTO Tasks(Subject,Message,Dailyquote,Dailyweather,Schedule,Channel,Location,Createdtime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'
    try:
        cursor.execute(sql, (subject,message,dailyquote,dailyweather,schedule,channel,location,date_time))
        DBConn.commit()
        saved_id = cursor.lastrowid
        log(f'TaskId {saved_id} has been saved in database!\nSubject: {subject}. \nMessage: {message}. \nSchedule: {schedule}.')
        return saved_id
    except Exception as err:
        DBConn.rollback()
        error(err)
        

def deletetask(taskid):
    sql = 'DELETE FROM Tasks Where Taskid = %s;'

    try:
        cursor.execute(sql, (taskid,))
        DBConn.commit()
        log(f'Removed Taskid {taskid} from DB.')

    except Exception as err:
        error(err)

def createconnection(saved_id,recipient_id):
    sql = 'INSERT INTO TaskRecipients(TaskId,RecipientId) VALUES (%s,%s);'

    try:
        cursor.execute(sql, (saved_id,recipient_id))
        DBConn.commit()
        log(f'TaskId {saved_id} has been connected to RecipientId {recipient_id}.')
        return
    except Exception as err:
        DBConn.rollback()
        error(err)
### END TASK MANAGER DB ACTIONS ###


### SCHEDULE MANAGER DB ACTIONS ###
def fetchtasks():
    cursor_dict.execute('''
    SELECT 
    tr.*, 
    t.*, 
    r.* 
    FROM Taskrecipients AS tr 
    INNER JOIN Tasks as t on tr.Taskid = t.Taskid 
    INNER JOIN Recipients as r on tr.RecipientId = r.RecipientId
    ORDER BY t.TaskId ASC;
    ''')
    records = cursor_dict.fetchall()  
    return records


def setlasttriggered(datetime,taskid):
    sql = 'UPDATE Tasks SET Lasttriggered = %s WHERE Taskid = %s;'

    try:
        cursor.execute(sql, (datetime,taskid))
        DBConn.commit()
        log(f'Last triggered updated to {datetime} On TaskId {taskid}.')
    except Exception as err:
        DBConn.rollback()   
        error(err)
### END SCHEDULE MANAGER DB ACTIONS ###


### PERFORMANCE MONITOR DB ACTIONS ###
def saveperformancerecord(operation_name,start_time,finish_time,taskid):
    sql = 'INSERT INTO Performance(Operation,Starttime,Finishtime,TaskId) VALUES(%s,%s,%s,%s)'
     
    try:
        cursor.execute(sql, (operation_name.title(),start_time,finish_time,taskid))
        DBConn.commit()
    except Exception as err:
        DBConn.rollback()
        error(err)
### END PERFORMANCE MONITOR DB ACTIONS ###


### REPORT CREATOR DB ACTIONS ###
def fetchperformancerecords(horizon):
    cursor_dict.execute(f'''
    SELECT 
    p.Id,
    p.Operation,
    p.Starttime,
    p.Finishtime,
    SUM(p.Finishtime - p.Starttime) as Operationtime
    FROM Performance as p
    WHERE Starttime LIKE "{horizon}%"
    GROUP BY Id
    Order by Id DESC
    ;
    ''')
    records = cursor_dict.fetchall()
    return records
