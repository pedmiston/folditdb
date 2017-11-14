def add_score(solution, session):
    score = solution.to_score_obj()
    session.add(score)
