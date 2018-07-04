import pytest

from blockex.tradeapi.helper import DictConditional, head


class TestDictConditional:
    def test_new_condition(self):
        dcond = DictConditional(__cond__=lambda x: x != 0)
        dcond["foo"] = 0
        assert "foo" not in dcond

        dcond = DictConditional(__cond__=lambda x: x != 0, a=1, b=2)
        dcond["foo"] = 0
        assert "foo" not in dcond
        assert "a" in dcond and "b" in dcond

    def test_default_cond_with_definition(self):
        dcond = DictConditional(a=1, b=2)
        dcond["smart_none"] = None
        assert "smart_none" not in dcond
        assert "a" in dcond and "b" in dcond


class TestGetFirst:
    def test_head(self):
        assert head([]) is None
        assert head(()) is None

        assert head((), default=[]) == []
        assert head((1, 2, 3)) == 1
