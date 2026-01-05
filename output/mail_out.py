import base64
from email.message import EmailMessage
from modules.logger import log,error

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2.credentials import Credentials

from config import GOOGLECRED, DRY_RUN_OUTPUT


def gmail_send_message(to='emil.sjoekvist@gmail.com', subject='Hej', content='Ett mail'):
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """


  try:
    if not DRY_RUN_OUTPUT:
      service = build("gmail", "v1", credentials=GOOGLECRED)
      message = EmailMessage()

      message.set_content(content)

      message["To"] = to
      message["From"] = "emil.sjokvist.hitachienergy@gmail.com"
      message["Subject"] = subject

      # encoded message
      encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

      create_message = {"raw": encoded_message}
      # pylint: disable=E1101
      send_message = (
          service.users()
          .messages()
          .send(userId="me", body=create_message)
          .execute()
      )
      log(f'E-mail with Id: {send_message["id"]} has been sent to {to}. Message: {content}.')
    else:
      log(f'Mail message output was triggered in Dry run mode! Subject: {subject}. Message: {content}. Recipient: {to}.')
      send_message = f'Mail message output was triggered in Dry run mode! Subject: {subject}. Message: {content}. Recipient: {to}.'
  except HttpError as err:
    error(f"An error occurred: {err}")
    send_message = None
  return send_message


if __name__ == "__main__":
  gmail_send_message()