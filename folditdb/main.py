import argparse
import json
from pathlib import Path
from folditdb.solution import Solution

def load_solutions(solutions):
    for solution_json in open(solutions):
        solution = Solution(json.loads(solution_json))
        print(solution.filename)

def main():
    parser = argparse.ArgumentParser('folditdb')
    parser.add_argument('solutions', help='file containing solution data in json')
    args = parser.parse_args()
    assert Path(args.solutions).exists(), 'solutions file does not exist'
    load_solutions(args.solutions)
