class Config:

    def __init__(self, devices):
        self.__DEVICES = devices
        self.__VETOED = []
        self.__MSG = None
        self.__VALID = b"the_key_is_valid"
        self.__END = b"end_keys"

    def valid_tag(self):
        return self.__VALID

    def end_tag(self):
        return self.__END

    def get_devices(self):
        return self.__DEVICES

    def veto(self, id: int):
        self.__VETOED.append(id)

    def get_vetoed(self):
        return self.__VETOED

    def encrypted(self, msg: bytes) -> None:
        self.__MSG = msg

    def get_encrypted(self) -> bytes:
        return self.__MSG
