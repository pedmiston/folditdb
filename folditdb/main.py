import argparse
from pathlib import Path

from folditdb.load import load_solutions

def main():
    parser = argparse.ArgumentParser('folditdb')
    parser.add_argument('solutions', help='file containing solution data in json')
    args = parser.parse_args()
    assert Path(args.solutions).exists(), 'solutions file does not exist'
    load_solutions(args.solutions)
