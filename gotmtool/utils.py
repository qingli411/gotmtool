#--------------------------------
# Utility
#--------------------------------

def inquire(message, default):
    """Inquire with message and default answer

    :message: (str) message for inquiry
    :default: (str) default answer for inquiry
    :returns: (str) answer

    """
    try:
        user_input = input(message+': ({})\n'.format(default))
    except SyntaxError:
        user_input = None
    if user_input is None or user_input.strip() == '':
        return default
    else:
        return user_input

def print_error(message):
    """Print error message in red

    :message: (str) error message

    """
    print('\033[91mERROR: '+message+'\033[0m')

def print_warning(message):
    """Print warning message in bluw

    :message: (str) warning message

    """
    print('\033[94mWARNING: '+message+'\033[0m')

def print_ok(message):
    """Print OK message in green

    :message: (str) OK message

    """
    print('\033[92m'+message+'\033[0m')

def print_hints(message):
    """Print hints

    :message: (str) hints

    """
    print('  '+message)
