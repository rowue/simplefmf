import nose
from nose.tools import raises, assert_almost_equal, ok_, eq_

from simplefmf import FMFDataDefinition

@raises(ValueError)
def test_FMFDataDefinition_init_no_definition():
    name="Test"
    object=FMFDataDefinition(name=name)

@raises(ValueError)
def test_FMFDataDefinition_init_no_name():
    definition="a(n)"
    object=FMFDataDefinition(definition=definition)


class TestDataDefinitionUse():
    def setUp(self):
        name="Test"
        definition="a(n)"
        self.object=FMFDataDefinition(name,definition)

    def test_get_definition(self):
        eq_(self.object.definition_entry, "Test: a(n)")


class TestDefaultMask():
    """Tests evaluating of default masks."""
    # Perhaps a dict would be nicer...
    def setUp(self):
        self.object = FMFDataDefinition("Test", "a(n)")

    def test_default_mask_string(self):
        self.object.default_mask("gaga")
        eq_(self.object.mask, "%s")

    def test_default_mask_bool(self):
        self.object.default_mask(True)
        eq_(self.object.mask, "%s")
        
    def test_default_mask_int(self):
        self.object.default_mask(3)
        eq_(self.object.mask, "%0d")
        
    def test_default_mask_float(self):
        self.object.default_mask(3.0)
        eq_(self.object.mask, "%.3e")
