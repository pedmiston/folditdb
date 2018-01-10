from os import remove
from pathlib import Path

import pytest

from folditdb import log, tables
from folditdb.load import load_irdata_from_file
from folditdb.irdata import IRData

@pytest.fixture
def tmp_log():
    """Configure folditdb to log to a temporary file."""
    tmp_log_filepath = 'tests/tmp_errors.log'
    log.use_logging(tmp_log_filepath)
    yield tmp_log_filepath
    remove(tmp_log_filepath)

def test_logger_records_irdata_property_error(tmp_log, session):
    load_irdata_from_file('tests/test_data/solutions_with_errors.json', session)
    assert len(open(tmp_log).readlines()) == 1

    error_log = open(tmp_log).read()
    expected_error_msg = 'IRDataPropertyError: solution has no HISTORY'
    assert expected_error_msg in error_log
