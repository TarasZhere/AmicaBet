def bet_logic_valid(votes):
    voted = [*set(map(lambda i: dict(i).get('voted_Uid'), votes))]

    if len(voted) > 1:
        return None

    return voted[0]
