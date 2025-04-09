from colorama import Back, Fore, Style


def print_color(color, text):
    '''
    Print dans la couleur voulue
    :param color: La couleur (formatée pour colorama) Fore.GREEN / Fore.BLUE etc...
    :param text: Le texte à afficher
    :return: None
    '''
    print(f"{color}{text}{Style.RESET_ALL}")


def print_green(text):
    '''
    Print en vert
    :param text: Le texte à afficher
    :return: None
    '''
    print_color(Fore.GREEN, text)


def print_red(text):
    '''
    Print en rouge
    :param text: Le texte à afficher
    :return: None
    '''
    print_color(Fore.RED, text)


def beauty_print(title, data):
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
