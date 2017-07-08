import unittest
from message_builders.message_builders import simple_message_builder


class TestSimpleMessageBuilder(unittest.TestCase):

    def setUp(self):
        pass

    def test_with_metadata(self):
            self.assertTrue("metadata" in simple_message_builder(message_text="message_text", metadata="metadata"))

    def test_without_metadata(self):
            self.assertFalse("metadata" in simple_message_builder(message_text="message_text"))

