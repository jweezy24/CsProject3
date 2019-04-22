import unittest
import sys
import server.Tree.Node as Node

class TestNodeMethods(unittest.TestCase):
    def setUp(self):
        self.node = Node("jweezy")

    def test_init(self):
        self.assertTrue(self.node.data == "jweezy")
        self.assertFalse(self.node.right)
        self.assertFalse(self.node.left)

    def test_set_l_child(self):
        tempNode = Node("test")
        self.assertFalse(self.node.left == tempNode)
        self.node.set_l_child(tempNode)
        self.assertTrue(self.node.left == tempNode)

    def test_set_r_child(self):
        tempNode = Node("test2")
        self.assertFalse(self.node.right == tempNode)
        self.node.set_r_child(tempNode)
        self.assertTrue(self.node.right == tempNode)

    def test_clear_children(self):
        tempNode = Node("test")
        tempNode2 = Node("test2")
        self.node.set_l_child(tempNode)
        self.node.set_r_child(tempNode2)
        self.assertTrue(self.node.right)
        self.assertTrue(self.node.left)
        self.node.clear_children()
        self.assertFalse(self.node.right)
        self.assertFalse(self.node.left)
unittest.main()
