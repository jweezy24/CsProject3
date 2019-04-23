from .Node import Node

class BTree(object):

    def __init__(self, root):
        if isinstance(root, Node):
            self.root = root
            self.size = 0
        else:
            raise ValueError('Cannot initalize tree without root node')

    def add_node(self, node):
        leafs = self.get_next_open_node(self.root)
        #print("printing leaves " + str(leaves) +" HERE ")
        if leafs:
            #print("printing Node in leaves " + str(leafs) +" HERE ")
            if leafs.left or leafs.right:
            #    print("in add node child")
                if leafs.left:
                    leafs.set_r_child(node)
                    self.set_parent(leafs, node)
                else:
                    leafs.set_l_child(node)
                    self.set_parent(leafs, node)
            else:
                leafs.set_l_child(node)
                self.set_parent(leafs, node)
        self.size += 1

    def set_parent(self, parent, child):
        if isinstance(parent, Node) and isinstance(child, Node):
            child.parent = parent
        else:
            raise ValueError('Child and/or parent not of type "Node".')

    def get_next_open_node(self, node):
        if not node.left or not node.right:
            if not node.left:
                return node
            elif not node.right:
                return node
            else:
                return node
        elif node.left and node.right:
            if self.size%2 == 0:
                return self.get_next_open_node(node.right)
            else:
                return self.get_next_open_node(node.left)
