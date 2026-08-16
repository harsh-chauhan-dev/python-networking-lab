def calculate_search_space(charset_size,password_length):
    """
    Search sapce = charset_size ^ password_length
    """
    if charset_size <=0:
        raise ValueError("Charset size must be geater then 0")

    if password_length <=0:
        raise ValueError("Password length be must be greater then 0")

    return charset_size ** password_length


def numeric_search_space(length):
    """
    Search space for numeric password.
    """
    return calculate_search_space(10,length)