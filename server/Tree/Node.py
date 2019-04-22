
class Node(object):
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

    def set_l_child(self, child):
        if isinstance(child, Node):
            if self.right:
                if self.right != child:
                    self.left = child
                    return True
                else:
                    return False
            else:
                self.left = child
                return True
        else:
            return False

    def set_r_child(self, child):
        if isinstance(child, Node):
            if self.left:
                if self.left != child:
                    self.right = child
                    return True
                else:
                    return False
            else:
                self.right = child
                return True
        else:
            return False

    def clear_children(self):
        self.right = None
        self.left = None

    #rewritting how the objects will compare
    def __eq__(self, other):
        if not other:
            return False
        else:
            if isinstance(other, Node):
                return self.data == other.data
        return False
