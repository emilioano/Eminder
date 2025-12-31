import mysql.connector
import json
import datetime
from modules.logger import log,debug,info,warning,error,critical
from modules import recipientmanager, aimanager

from config import DBCONFIG

import re

DBConn = mysql.connector.connect(**DBCONFIG);
cursor = DBConn.cursor()

airesponse = r"""```json
{
    "answers": [
        {
            "Subject": "Cosmic Wonder Watch",
            "Message": "Tonight, take a break from the ordinary! Step outside, find a dark spot away from city lights, and look up at the night sky. Witness the silent dance of stars, planets, and maybe even a meteor shower. Consider bringing a warm blanket, a thermos of hot chocolate, and a pair of binoculars for an enhanced experience. Let the universe inspire you!",
            "schedule": {
                "time": "20251230 20:16",
                "type": "once",
                "timezone": "CET"
            }
        }
    ]
}
```
"""
    
            

print(airesponse)



airesponse_regex = re.sub(r"```(?:json)?", "", airesponse).strip()

print(f'Regex: {airesponse_regex}')


jsonresponse = json.loads(airesponse_regex)
answers = jsonresponse["answers"]

#print(f'Answers: {jsonresponse["answers"]}')


savepost = input('Do you want to save this record(s)? Y/N')

if savepost == "Y":
    now_str = str(datetime.datetime.now())
    date_time = (now_str.split('.')[0])
    sql = 'INSERT INTO Tasks(Message,Dailyquote,Dailyweather,Schedule,Channel,Location,Createdtime) VALUES (%s,%s,%s,%s,%s,%s,%s);'

    #i = 1
    for answer in answers:
        #print(f'Id: {i}')
        #print(answer["Subject"])
        #print(answer["Text"])
        #print(answer["schedule"])

        text = answer["Message"]
        schedule = answer["schedule"]

        #i+=1

        try:
            cursor.execute(sql, (text,'0','0',json.dumps(schedule),'1','',date_time))
            DBConn.commit()
            saved_id = cursor.lastrowid

            log(f'TaskId {saved_id} has been saved! Message: {answer["Message"]}. Schedule: {answer["schedule"]}.')

            recipient_question = str(input('Recipients (1. Add new. 2. Add recipient from existing): '))
            if recipient_question == str(1):
                recipientmanager.run_recipient_program(saved_id)
            if recipient_question == str(2):
                selection = 4


        except Exception as err:
            error(err)

