import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(tag="p", value="algo", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_values(self):
        node= HTMLNode(
            tag="div",
            value="benjimosso"
        )
        self.assertEqual(
            node.tag,
            "div"
        )
        self.assertEqual(
            node.value,
            "benjimosso"
        )
        self.assertEqual(
            node.children,
            None
        )
        self.assertEqual(
            node.props,
            None
        )
    def test_repr(self):
        node= HTMLNode(
            "p",
            "Hola mijo",
            "None",
            {"class": "primary"}
        )
        self.assertEqual(
            node.__repr__(),
            "HTML Node(p, Hola mijo, children: None, {'class': 'primary'})"
        )

if __name__ == "__main__":
    unittest.main()