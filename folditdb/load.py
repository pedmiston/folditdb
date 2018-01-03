from folditdb.irdata import IRData

def load_solutions(solutions):
    for solution_json in open(solutions):
        solution = IRData.from_json(solution_json)
        print(solution.filename)
