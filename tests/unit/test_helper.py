from unittest import TestCase

from blockex.tradeapi.helper import DictConditional, head


class TestDictConditional(TestCase):
    def test_new_condition(self):
        dcond = DictConditional(__cond__=lambda x: x != 0)
        dcond["foo"] = 0
        self.assertTrue("foo" not in dcond)

        dcond = DictConditional(__cond__=lambda x: x != 0, a=1, b=2)
        dcond["foo"] = 0
        self.assertTrue("foo" not in dcond)
        self.assertTrue("a" in dcond and "b" in dcond)

    def test_default_cond_with_definition(self):
        dcond = DictConditional(a=1, b=2)
        dcond["smart_none"] = None
        self.assertTrue("smart_none" not in dcond)
        self.assertTrue("a" in dcond and "b" in dcond)


class TestGetFirst(TestCase):
    def test_head(self):
        self.assertEqual(head([]), None)
        self.assertEqual(head(()), None)

        self.assertEqual(head((), default=[]), [])
        self.assertEqual(head((1, 2, 3)), 1)
