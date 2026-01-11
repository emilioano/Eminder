from eminder.db.dbactions import viewtasks, viewrecipients, fetchtasks, fetchperformancerecords
from eminder.db import dbactions

import pytest
import mysql.connector
from eminder.config import DBCONFIG

from unittest.mock import patch

# Testing that the Read operations from db does not result in error. This test runs only locally
@pytest.mark.skip_in_ci
@patch("eminder.db.dbactions.error")
def test_read_db(mock_error):
    viewtasks()
    viewrecipients()
    fetchtasks()
    fetchperformancerecords('Today')
    mock_error.assert_not_called()

