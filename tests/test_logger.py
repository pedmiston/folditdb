from os import remove
from pathlib import Path

import pytest

from folditdb import log, tables
from folditdb.load import load_top_solutions_from_file
from folditdb.irdata import IRData

def test_logger_records_irdata_property_error(tmp_log, session):
    load_top_solutions_from_file('tests/test_data/solutions_with_errors.json', session)

    error_log = open(tmp_log).read()
    expected_error_msg = 'IRDataPropertyError(solution has no HISTORY'
    assert expected_error_msg in error_log
