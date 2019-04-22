import Node

class BTree:

    def __init__(self, root, size):
        if isinstance(root, Node):
            self.root = root
            self. size = size
        else:
            raise ValueError('Cannot initalize tree without root node')

    def add_node(self, val):
        pass

    def get_newest_position(self):
        pass
