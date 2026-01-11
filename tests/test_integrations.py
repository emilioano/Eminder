import pytest
from unittest.mock import patch
from eminder.integrations.discord_out import discord_send_message
from eminder.integrations.mail_out import gmail_send_message
from eminder.integrations.aimanager import AIprompt

import json
from unittest.mock import patch



# Testing discord_out
@patch('eminder.integrations.discord_out.DRY_RUN_OUTPUT', True)
@patch("eminder.integrations.discord_out.log")
def test_discordout(mock_log):
    discord_send_message('https://fakewebhook','Test message')
    mock_log.assert_called_once()
    assert 'Discord message output was triggered in Dry run mode!' in mock_log.call_args[0][0]

# Testing mail_out
@patch('eminder.integrations.mail_out.DRY_RUN_OUTPUT', True)
@patch("eminder.integrations.mail_out.log")
def test_mailout(mock_log):
    gmail_send_message()
    mock_log.assert_called_once()
    assert 'Mail message output was triggered in Dry run mode!' in mock_log.call_args[0][0]

# Testing ai_manager
@patch("eminder.integrations.aimanager.requests.post")
@patch("eminder.integrations.aimanager.os.getenv")
@patch("eminder.integrations.aimanager.date_time", "2026-01-11 12:00") 
def test_aiprompt_success(mock_getenv, mock_post):
    mock_getenv.return_value = "DUMMY_KEY"

    fake_json = json.dumps({
        "answers": [
            {
                "Subject": "Gym: Push",
                "Message": "Måndag 18:00",
                "schedule": {"time": "18:00", "type": "weekly", "days": "mon"}
            }
        ]
    })

    mock_post.return_value.status_code = 200
    mock_post.return_value.text = fake_json
    mock_post.return_value.json.return_value = {
        "candidates": [
            {"content": {"parts": [{"text": fake_json}]}}
        ]
    }

    out_text = AIprompt("Ge mig ett program.")
    data = json.loads(out_text)

    mock_getenv.assert_called_with("gemini_api_key")
    mock_post.assert_called_once()
    assert data["answers"][0]["Subject"] == "Gym: Push"
    assert data["answers"][0]["schedule"]["type"] == "weekly"
