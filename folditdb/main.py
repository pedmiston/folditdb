import argparse
from pathlib import Path

from folditdb.db import DB, Session
from folditdb.tables import Base
from folditdb.load import load_solutions_from_file


def main():
    parser = argparse.ArgumentParser('folditdb')
    parser.add_argument('solutions', help='file containing solution data in json')

    args = parser.parse_args()
    assert Path(args.solutions).exists(), 'solutions file does not exist'

    load_solutions_from_file(args.solutions)
