from colors import Colors


def help():
    print(f"""
    options:
        {Colors.BOLD}{Colors.BLUE}a{Colors.END}  -  Decrypts the message with all devices
        {Colors.BOLD}{Colors.BLUE}d{Colors.END}  -  Decrypts the message with a particular device
        {Colors.BOLD}{Colors.BLUE}e{Colors.END}  -  Exit the program
        {Colors.BOLD}{Colors.BLUE}h{Colors.END}  -  Displays this help menu""")

def list_to_str(list_to_print):
    list_to_print = list(dict.fromkeys(list_to_print))
    if len(list_to_print) == 0:
        string = '[]'
    else: 
        string = ', '.join(map(str, list_to_print))
    return string

def summary(values: dict):
    print(f"""
    ================= Summary =================
        {Colors.BOLD}Devices    :{Colors.END} {values['n']}
        {Colors.BOLD}Message    :{Colors.END} {values['m'].decode('ascii')}
        {Colors.BOLD}Vetoed     :{Colors.END} {list_to_str(values['vetoed'])}  ({list_to_str(values['real'])})
        {Colors.BOLD}Cover of S :{Colors.END} {list_to_str(values['cover'])}
        {Colors.BOLD}Padded msg :{Colors.END} {values['p']}
    ===========================================
          """)

def danger_icon():
    return f'{Colors.RED}{Colors.BOLD}[!]{Colors.END}'


def info_icon():
    return f'{Colors.YELLOW}{Colors.BOLD}[*]{Colors.END}'


def tick_icon():
    return f'{Colors.GREEN}{Colors.BOLD}[✓]{Colors.END}'


def print_info(info: str):
    print(f'\n\t{info_icon()}{Colors.YELLOW} {info}{Colors.END}\n')


def print_error(error: str):
    print(f'\n\t{danger_icon()} {Colors.RED}{error}{Colors.END}\n')


def print_with_name(name: str, value):
    print(f'\t{Colors.BOLD}{Colors.GREEN}{name.ljust(25)}{Colors.END}  -  {value}')

def print_success(num: int, msg: str):
    print(f'\t{tick_icon()} {Colors.GREEN}Device {str(num).ljust(3)} - {msg}{Colors.END}')


def print_unsuccess(num: int):
    print(f'\t{danger_icon()} {Colors.RED}Device {str(num).ljust(3)} - Was unable to decrypt{Colors.END}')