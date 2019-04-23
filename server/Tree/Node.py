
class Node(object):
    def __init__(self, data):
        self.data = data
        self.parent = None
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

    def __str__(self,level=1):
        if isinstance(self.left, Node):
            tempLevel = level
            tempLevel +=1
            left = str("\n")+ str("\t"*level) + self.left.__str__(tempLevel) + ""
        else:
            left = ""
        if isinstance(self.right, Node):
            tempLevel = level
            tempLevel +=1
            right = str("\n")+ str("\t"*level) + self.right.__str__(tempLevel)
        else:
            right = ""
        return "Node: " + str(self.data) + str(left)  + str(right)


    #rewritting how the objects will compare
    def __eq__(self, other):
        if not other:
            return False
        else:
            if isinstance(other, Node):
                return self.data == other.data
        return False
