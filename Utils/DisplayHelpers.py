from colorama import Back, Fore, Style


def print_color(color, text):
    """
    Print in the desired color
    :param color: The color (formatted for colorama) Fore.GREEN / Fore.BLUE etc...
    :param text: The text to display
    :return: None
    """
    print(f"{color}{text}{Style.RESET_ALL}")


def print_green(text):
    """
    Print in green
    :param text: The text to display
    :return: None
    """
    print_color(Fore.GREEN, text)


def print_red(text):
    """
    Print in red
    :param text: The text to display
    :return: None
    """
    print_color(Fore.RED, text)


def beauty_print(title, data):
    """
    Nicely format and print a title and its associated data
    :param title: The title to display
    :param data: The data to display (can be a list, dict, or other types)
    :return: None
    """
    title_len = len(title)
    star_line = "-" * title_len
    #print_red(f"{star_line}")
    print_red(f"{title}")
    #print_red(f"{star_line}")
    if type(data) in (list, int, float, str, bool):
        print(data)
    elif type(data) == dict:
        for k, v in data.items():
            print(f"{k}:{v}")
    #print(100*"*")
    #print()