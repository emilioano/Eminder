from eminder.utils import log,debug,info,warning,error,critical
from eminder.config import DRY_RUN_OUTPUT,DISCORD_WEBHOOK_ADMIN


import requests

def discord_send_message(webhook='None',content='Hej'):

    if not webhook:
        if not DISCORD_WEBHOOK_ADMIN:
            error(f'There is no webhook provided to send any notification to discord, please check setup! Message: {content}.')
            return
        else:
            webhook=DISCORD_WEBHOOK_ADMIN
            content=f'Message is sent to admin to check as the recipients webhook is not properly setup! {content}.'
            error(f'Message is sent to admin to check as the recipients webhook is not properly setup! {content}.')

    webhook_url = webhook
    data = {
        "content": content,
        "username": "Eminder Bot"
    }

    if not DRY_RUN_OUTPUT:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            log("Message sent successfully via Discord: {content}")
        else:
            error(f"Error code: {response.status_code}. Error response text: {response.text}")
    else:
        log(f'Discord message output was triggered in Dry run mode! Message: {content}')





if __name__ == '__main__':
    discord_send_message(DISCORD_WEBHOOK_ADMIN,'Alert from Eminder!')
