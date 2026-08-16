def estimate_second(search_space,attempts_per_second):
    """
    Estimate the time required to search the entire space.
    """
    if attempts_per_second <=0:
        raise ValueError("Attempts per second must be greater then 0")

    return search_space/attempts_per_second


def format_time(second):
    """
    Convert second into a readable format.
    """

    if second <1:
        return f"{second:.4f} seconds"

    if second <60:
        return f"{second:.2f} seconds"

    minutes = second/60

    if minutes < 60:
        return f"{minutes:.2f} mintes"

    hours = minutes/60

    if hours<24:
        return f"{hours:.2f} hours"

    days = hours/24

    return f"{days:.2f} days"
