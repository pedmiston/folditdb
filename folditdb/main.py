import argparse
from pathlib import Path
import logging

from folditdb.load import load_solutions

logger = logging.getLogger(__name__)
handler = logging.FileHandler('folditdb-errors.csv')
logger.addHandler(handler)

def main():
    parser = argparse.ArgumentParser('folditdb')
    parser.add_argument('solutions', help='file containing solution data in json')
    args = parser.parse_args()
    assert Path(args.solutions).exists(), 'solutions file does not exist'
    load_solutions(args.solutions)
