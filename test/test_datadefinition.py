import nose
from nose.tools import raises, assert_almost_equal, ok_, eq_

from simplefmf import FMFDataDefinition

def test_FMFDataDefinition_init():
    name="Test"
    definition="a(n)"

    object=FMFDataDefinition(name=name, definition=definition)
    eq_(object.name, name)
    eq_(object.definition, definition)

def test_FMFDataDefinition_assign():
    name="Test"
    definition="a(n)"

    object=FMFDataDefinition()

    object.name=name
    object.definition=definition
    eq_(object.name, name)
    eq_(object.definition, definition)

def test_FMFDataDefinition_get_definition():
    name="Test"
    definition="a(n)"

    object=FMFDataDefinition()
    object.name=name
    object.definition=definition
    eq_(object.get_definition(), "Test: a(n)")

