def confidence_score(value):
    if not value:
        return 0.0
    if len(value) > 5:
        return 0.9
    return 0.6
