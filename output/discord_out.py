from modules.logger import log,debug,info,warning,error,critical

import requests

def discord_send_message(webhook='None',content='Hej'):

    webhook_url = webhook
    data = {
        "content": content,
        "username": "Eminder Bot"
    }

    response = requests.post(webhook_url, json=data)
    

    if response.status_code == 204:
        log("Message sent!")
    else:
        error(f"Error code: {response.status_code}. Error response text: {response.text}")


if __name__ == '__main__':
    discord_send_message('https://discord.com/api/webhooks/1455953105819799729/DJeIBLrw4NGsHqNpMU4J04cg_GAE0WgVwShFbhjxehqSkNltwMpVSiBhU2ThRx9i5eee','Alert from Eminder!')
