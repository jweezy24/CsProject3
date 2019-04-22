import server.Tree.BTree as BTree
import server.Tree.Node as Node

#size refers to the nodes
def generate_tree(size):
    root = Node("0")
    tree = BTree(root, size)
    for i in range(1,size):
        tempNode = Node(str(i))
        tree.add_node(Node(str(i)))
    return tree

if __name__ == "__main__":
    tree = generate_tree(16)
    print(tree.root)
