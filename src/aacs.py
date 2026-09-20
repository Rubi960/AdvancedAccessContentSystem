from crypto import (
    complete_block,
    decrypt_aes,
    encrypt_aes,
    get_random_key,
    remove_extra,
)

from config import Config
from print import help, summary, print_error, print_info, print_success, print_unsuccess
from tree import Tree


class AACS:

    def __init__(self, config: Config, tree: Tree):
        self.config = config
        self.tree = tree

    def get_cover_s(self):
        cover_s = []
        not_possible = [1]
        valid = []

        if len(self.config.get_vetoed()) == 0:
            cover_s = [1]
        else:
            for i in self.config.get_vetoed():
                id = self.tree.get_real_id(i)
                root_path = self.tree.root_route(id)
                # The root is not taken into consideration in this case
                for j in root_path[:-1]:
                    not_possible.append(j)
                    valid.append(self.tree.get_sibling_id(j))

            for val in valid:
                if val not in not_possible:
                    cover_s.append(val)
        return sorted(cover_s)

    """
    Generate k
    Encrypt k with each kn of cover of S
    Encrypt the message with k
    Put together all the keys encrypted with kn and the original message

    Important, as blocks of 16 are encrypted, if my validkey tag was bigger
    than 16, it would have 32 bytes directly.

    16 bytes iv + 'thiskeyisvalid' + 16 bytes of k
    """
    def encrypt_process(self, m: bytes) -> bytes:
        k = get_random_key()

        keys = []
        for u in self.get_cover_s():
            k_u = self.tree.get_node(u)
            # The encrypt function returns the iv and the encrypted key.
            # And since we have to pass both of them, we put them together
            # in the same string
            # That is, I have 16 bytes iv + 'the_key_is_valid' + 16 bytes of k
            # for each k until I get to end (48 bytes for each key).
            keys.append(b"".join(encrypt_aes(k_u, self.config.valid_tag() + k)))

        # Here we are going to have 'end_keys' + 16 bytes iv +  message
        c = b"".join(encrypt_aes(k, complete_block(m)))

        return b"".join(keys) + self.config.end_tag() + c

    def decrypt_process(self, device: int):
        loop = True
        k = None
        m = None
        c = self.config.get_encrypted()
        while loop:
            if c.startswith(b"end_keys"):
                loop = False
                break
            iv_u, k_c = c[:16], c[16:48]
            for path in self.tree.root_route(device):
                k_u = self.tree.get_node(path)
                d = decrypt_aes(k_u, iv_u, k_c)
                if d.startswith(self.config.valid_tag()):
                    k = d[16:]
                    break
            c = c[48:]

        if k is not None:
            c = c[len(self.config.end_tag()) :]
            m = remove_extra(decrypt_aes(k, c[:16], c[16:]))
        return m

    def ask_for_device(self):
        n = 0
        while n < 1 or n > self.config.get_devices():
            try:
                val = input(f'Device number ({1}/{self.config.get_devices()}): ')

                if val == '':
                    n = None
                    break

                n = int(val)
            except ValueError:
                print_error("Invalid entry. The value must be numeric.")
        return n

    def veto_devices(self):
        loop = True
        print_info('Enter a device number or Enter to finish')
        while loop:
            n = self.ask_for_device()

            if n is None:
                loop = False
                break

            if n in self.config.get_vetoed():
                print_error('The device is already vetoed')
            else:
                print_info(f'The device {n} has been vetoed.')
                self.config.veto(n)


def get_message():
    msg = ''
    while msg == '':
        msg = input('Message: ')
    return msg.encode('ascii')


def get_n_devices():
    try:
        n = int(input('Number of devices or enter for default (8): ') or 8)
    except ValueError:
        print_error("Invalid entry. Value must be numeric.")
        exit(1)
    return n if n > 1 else 1


def decrypt_with_device(aacs: AACS, device: int):
    device_id = aacs.tree.get_real_id(device)
    dec = aacs.decrypt_process(device_id)
    if dec is None:
        print_unsuccess(device)
    else:
        print_success(device, dec.decode('ascii'))


def init():
    print()
    config = Config(get_n_devices())
    t = Tree(config.get_devices())
    return config, t

def main(aacs: AACS):

    # Add devices to the restricted list
    aacs.veto_devices()
    print()

    # Encrypts a specific message
    m = get_message()
    c = aacs.encrypt_process(m)
    aacs.config.encrypted(c)

    # Print info for this execution
    vetoed = aacs.config.get_vetoed()
    summary(values={
        'n': aacs.config.get_devices(),
        'm': m,
        'p': complete_block(m),
        'vetoed': vetoed,
        'real': map(aacs.tree.get_real_id, vetoed),
        'cover': aacs.get_cover_s(),
    })

    loop = True
    help()

    while loop:
        option = input("\n\t> ")
        print()

        if option == 'a' or option == 'A':
            # Decrypts the message with all devices
            for device in range(1, aacs.config.get_devices() + 1):
                decrypt_with_device(aacs, device)

        elif option == 'd' or option == 'D':
            # Decrypts the message with a particular device
            device = None
            while device is None:
                device = aacs.ask_for_device()

            print()
            decrypt_with_device(aacs, device)

        elif option == 'e' or option == 'E':
            # Exit the program
            loop = False
            print_info('Exiting...')

        elif option == 'h' or option == 'H':
            # Displays this help menu
            help()


if __name__ == "__main__":
    config, tree = init()
    aacs = AACS(config, tree)
    main(aacs)
