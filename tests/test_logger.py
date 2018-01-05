from os import remove
from pathlib import Path

import pytest

from folditdb import log
from folditdb.irdata import IRData

@pytest.fixture
def tmp_log():
    """Configure folditdb to log to a temporary file."""
    tmp_log_filepath = 'tests/tmp_errors.log'
    log.use_logging(tmp_log_filepath)
    yield tmp_log_filepath
    remove(tmp_log_filepath)

def test_logger_records_irdata_property_error(tmp_log):
    irdata = IRData.from_file('tests/test_data/solution_without_history.json')
    irdata.to_model_object('Solution')  # should print error to log file
    error_log = open(tmp_log).read()
    expected_error_msg = 'IRData property error: solution has no history'
    assert expected_error_msg in error_log

def test_logger_records_irdata_property_error_only_once(tmp_log):
    irdata = IRData.from_file('tests/test_data/solution_without_history.json')
    irdata.to_model_object('Solution')  # should print error to log file
    assert len(open(tmp_log).readlines()) == 1
