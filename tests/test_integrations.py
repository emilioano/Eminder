import pytest
from unittest.mock import patch
from eminder.integrations.discord_out import discord_send_message

testcontent = 'This is testscript running with Pytest'

@patch('eminder.integrations.discord_out.DRY_RUN_OUTPUT', True)
@patch("eminder.integrations.discord_out.log")
## Test scripts for integration functions
def test_discordout(mock_log):
    discord_send_message('https://fakewebhook',testcontent)
    mock_log.assert_called_once()
    assert 'Discord message output was triggered in Dry run mode!' in mock_log.call_args[0][0]
