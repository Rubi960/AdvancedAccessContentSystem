from crypto import get_random_key
import math


class Tree:

    def __init__(self, devices: int) -> None:

        h = math.ceil(math.log2(devices)) + 1
        n = (2 ** h - 1) - (2 ** (h - 1) - devices)
        self.__n = n
        self.__height = h
        self.__nodes = {}
        self.__first = 1
        self.__last = n

        for i in range(1, self.__last + 1):
            self.__nodes[i] = get_random_key()

    def get_height(self):
        return self.__height

    def get_parent_id(self, id: int) -> int:
        return id // 2

    def get_sibling_id(self, id: int) -> int:
        if id == self.__first:
            return self.__first
        return (id + 1) if id % 2 == 0 else (id - 1)

    def get_node(self, id: int) -> bytes:
        return self.__nodes[id]

    def get_real_id(self, device: int) -> int:
        return 2 ** (self.__height - 1) + (device - 1)

    def get_nodes(self) -> dict:
        return self.__nodes

    def root_route(self, id: int) -> list[int]:
        route = [id]
        while id != self.__first:
            id = self.get_parent_id(id)
            route.append(id)
        return route


"""
         1
    2          3
 4    5     6     7
8 9 10 11 12 13 14 15
"""
