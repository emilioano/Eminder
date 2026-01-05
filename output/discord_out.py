from modules.logger import log,debug,info,warning,error,critical
from config import DRY_RUN_OUTPUT

import requests

def discord_send_message(webhook='None',content='Hej'):

    if not webhook:
        webhook='https://discord.com/api/webhooks/1455953105819799729/DJeIBLrw4NGsHqNpMU4J04cg_GAE0WgVwShFbhjxehqSkNltwMpVSiBhU2ThRx9i5eee'
        content=f'Message is sent to admin to check as the recipients webhook is not properly setup! {webhook}.'
        error(f'Message is sent to admin to check as the recipients webhook is not properly setup! {webhook}.')

    webhook_url = webhook
    data = {
        "content": content,
        "username": "Eminder Bot"
    }

    if not DRY_RUN_OUTPUT:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            log("Message sent!")
        else:
            error(f"Error code: {response.status_code}. Error response text: {response.text}")
    else:
        log(f'Discord message output was triggered in Dry run mode! Message: {content}')





if __name__ == '__main__':
    discord_send_message('https://discord.com/api/webhooks/1455953105819799729/DJeIBLrw4NGsHqNpMU4J04cg_GAE0WgVwShFbhjxehqSkNltwMpVSiBhU2ThRx9i5eee','Alert from Eminder!')
