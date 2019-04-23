import unittest
import sys
import server.Tree.Node as Node

class TestNodeMethods(unittest.TestCase):
    def setUp(self):
        self.node = Node.Node("jweezy")
        self.tempNode = Node.Node("test")
        self.tempNode2 = Node.Node("test2")

    def test_init(self):
        self.assertTrue(self.node.data == "jweezy")
        self.assertFalse(self.node.right)
        self.assertFalse(self.node.left)
        self.assertFalse(self.node.parent)

    def test_set_l_child(self):
        self.assertFalse(self.node.left == self.tempNode)
        self.node.set_l_child(self.tempNode)
        self.assertTrue(self.node.left == self.tempNode)

    def test_set_r_child(self):
        self.assertFalse(self.node.right == self.tempNode2)
        self.node.set_r_child(self.tempNode2)
        self.assertTrue(self.node.right == self.tempNode2)

    def test_clear_children(self):
        self.node.set_l_child(self.tempNode)
        self.node.set_r_child(self.tempNode2)
        self.assertTrue(self.node.right)
        self.assertTrue(self.node.left)
        self.node.clear_children()
        self.assertFalse(self.node.right)
        self.assertFalse(self.node.left)

    def test_str(self):
        self.assertEqual(str(self.node), 'Node: jweezy') # wanna change this, omw over rn

    def test_eq(self):
        eq_node = Node.Node('test')
        self.assertNotEqual(self.tempNode, self.tempNode2)
        self.assertEqual(self.tempNode, eq_node)

unittest.main()
