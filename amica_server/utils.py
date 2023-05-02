import re


REGX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def validEmail(email):
    '''
        Returns true if email if valid. Else False
    '''
    if re.fullmatch(REGX, email):
        return True
    return False

def invalidPassword(password):

    if (len(password)<=8):
        return 'Password must be of lenth 8 or more'

    elif not re.search("[a-z]", password):
        return 'Password must contain at lease a lower case digit'

    elif not re.search("[A-Z]", password):
        return 'Password must contain at lease a upper case digit'

    elif not re.search("[0-9]", password):
        return 'Password must contain at lease a digit 0-9'

    else:
        return None
