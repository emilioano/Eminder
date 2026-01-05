import requests
import json
from dotenv import load_dotenv
import os
import re

from modules.logger import log,debug,info,warning,error,critical


debug = False

load_dotenv(override=True)

### Prompt to AI

def AIprompt(prompt):

    askprompt = f'''

{prompt}

IMPORTANT: the reponse needs to be formatted in valid JSON only! Return ONLY valid JSON. 
Do not include code fences (```), language markers, or any extra text before or after the JSON.

MANDATORY: Place a short action description in "Subject", what to be done.
MANDATORY: Please place a detailed description in "Message", when to do the activity(s) and why. 

Available options for "type": once, daily, weekly, monthly, interval, yearly.
In case once, input in "time", format should be: YYYY-MM-DD HH:MM.
In case daily, input in "time", format should be: HH:MM.
In case weekly, input in "time", format should be HH:MM, and input in "Days" format should be the first three letters of the weekday, separated by comma, example: "mon,tue,thu,sat",
In case monthly, input in "time", format should be HH:MM and input in "Days" format should be the date of the month, example: "15" or "9".
In case interval, input in "time", format should be HH:MM and interval should correspond to the interval which number of days before it gets triggered again. Example: For everyday "1", every other day "2" etc.
In case yearly, input in "time", format should be: YYYY-MM-DD HH:MM and represent the first occurance for the task which will repeat yearly. 

You can put multiple tasks inside "answers" if required, return a single JSON object with an array of answers!

Do not put anything additional in the answer outside of the JSON object:

Following is the exact format and nothing should come before {{ or after}}:

{{   
    "answers":
        [
            {{"Subject":"...","Message":"...",{{schedule:"time":"...","type":"...","days":"...","interval":"...","timezone":"CET"}}}}
        ]

}}
    
'''


    print('Loading...')
    gemini_api_key = os.getenv('gemini_api_key')

    if debug:
        print('Prompt to AI: ',askprompt)
        print(f'API key: {gemini_api_key}')

    ai_endpoint = f'https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={gemini_api_key}'
    headers = {
        "Content-Type": "application/json"
    }

    aidata = {'contents':[
        {'parts':[{'text':askprompt}
    ]}]}
    airesponse = requests.post(ai_endpoint,headers=headers,data=json.dumps(aidata),verify=False)
    if airesponse.status_code==200:
        airesult = airesponse.json()
        airesulttext = airesult['candidates'][0]['content']['parts'][0]['text']

        # Sometimes the AI LLM returns some scrap characters shit even I asked specifically not to. Using regex to clean.
        airesponse_regex = re.sub(r"```(?:json)?", "", airesulttext).strip()

        print(airesponse_regex)
        return airesponse_regex

    else:
        error('Error ',airesponse.status_code,airesponse.text)
        return 'Error',airesponse.status_code,airesponse.text
        
if __name__ == '__main__':
    #AIprompt('Give me a watering schedule for my Jukka Brevifolia.')
    AIprompt('Give me a gym schedule, I want to start with Push, pull, legs.')
    