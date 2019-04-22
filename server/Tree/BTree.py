from .Node import Node

class BTree(object):

    def __init__(self, root, size):
        if isinstance(root, Node):
            self.root = root
            self.size = size
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
        else:
            if not self.root.left:
                self.root.set_l_child(node)
                self.set_parent(self.root, node)
            else:
                self.root.set_r_child(node)
                self.set_parent(self.root, node)

    def set_parent(self, parent, child):
        if isinstance(parent, Node) and isinstance(child, Node):
            child.parent = parent
        else:
            raise ValueError('Child and/or parent not of type "Node".')

    def get_next_open_node(self, node):
        if node.left and node.right:
            if not self.get_next_open_node(node.left).left or not self.get_next_open_node(node.left).right:
                return self.get_next_open_node(node.left)
            elif not self.get_next_open_node(node.right).left or not self.get_next_open_node(node.right).right:
                return self.get_next_open_node(node.right)
        elif not node.left or not node.right:
            return node


    
