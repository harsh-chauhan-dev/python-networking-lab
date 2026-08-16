from itertools import product


def generate_charset(length,charset):
    """
    Generate candidates using the the supplied charcter set.

    Example:
         charset = "01"
         length = 3

         000
         001
         010
         ...
         111   
    """

    if length <=0:
        raise ValueError("Length must be geater then 0")

    if not charset:
        raise ValueError("Charset can't be empty")

    for combination in product(charset,repeat=length):
        yield "".join(combination)

