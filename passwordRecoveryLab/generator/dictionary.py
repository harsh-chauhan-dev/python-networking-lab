def generate_dictionary(filename):
    """
    Read candidate password from a local dictionary file.
    """
    with open(filename,"r",encoding="utf-8") as file:
        for line in file:
           candidate = line.strip()

           if candidate:
               yield candidate

               