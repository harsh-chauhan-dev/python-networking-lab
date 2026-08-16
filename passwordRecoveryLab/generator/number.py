def generate_numeric(length):
    """
    Generate all numeric candidates of a given length.

    Example:
        lenght=4
        0000
        0001

        ....
        9999

    """
    if length <=0:
        raise ValueError("Length must be greater than 0")

    maximum = 10 **length

    for number in range(maximum):
        yield f"{number:0{length}d}"
