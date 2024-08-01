class Node:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and (other.__repr__() == self.__repr__())
