import nose
from nose.tools import raises, assert_almost_equal, ok_, eq_, assert_true, \
        assert_false
# test to check FMFTable
from simplefmf import FMFTable, FMFDataDefinition

class TestTableBasic():
    def setUp(self):
        self.table=FMFTable(name="Test", symbol="\tau")

    def test_table_name(self):
        eq_(self.table.name, "Test")

    def test_table_symbol(self):
        eq_(self.table.symbol, "\tau")

    def test_table_entry(self):
        eq_(self.table.table_entry, "Test: \tau")

class TestTableDefinitions():
    def setUp(self):
        self.table=FMFTable(name="Test", symbol="\tau")
        self.table.add_data_definition({'Bias Voltage':'U_1 [mV]'})
        self.table.add_data_definition('Acceleration Voltage','U_2(U_1) [kV]')
        self.table.add_data_definition('some stupid comment')
        a=FMFDataDefinition(name="Beam Current", definition="I_B(U_1) [mA]")
        self.table.add_data_definition(a)

    def test_data_definition_types(self):
        data_list = self.table.data_definitions
        assert_true(isinstance(data_list[0], FMFDataDefinition))
        assert_true(isinstance(data_list[1], FMFDataDefinition))
        assert_false(isinstance(data_list[2], FMFDataDefinition))
        assert_true(isinstance(data_list[2], str))
        assert_true(isinstance(data_list[3], FMFDataDefinition))

    def test_data_definition_out(self):
        data_list = self.table.table_definition(";")
        eq_(data_list[0], "[*data definitions: \tau]")
        eq_(data_list[1], "Bias Voltage: U_1 [mV]")
        eq_(data_list[2], "Acceleration Voltage: U_2(U_1) [kV]")
        eq_(data_list[3], "; some stupid comment")
        eq_(data_list[4], "Beam Current: I_B(U_1) [mA]")

class TestTableConsistency():
    def setUp(self):
        self.table=FMFTable(name="Test", symbol="\tau")
        self.table.add_data_definition({'Bias Voltage':'U_1 [mV]'})
        self.table.add_data_definition('Acceleration Voltage','U_2(U_1) [kV]')
        self.table.add_data_definition('some stupid comment')

    def test_consistency_overcols(self):
        self.table.data=[(1,2,3),(1,2,3), (3,2,1)]
        assert_false(self.table.verify_consistency())

    def test_consistency_uneqalrows(self):
        self.table.data=[(1,2,3),(1,2)]
        assert_false(self.table.verify_consistency())

    def test_consistency_ok(self):
        self.table.data=[(1,2,3),(1,2,3)]
        assert_true(self.table.verify_consistency())

# class TestTableMask():
#    def setUp(self):
        self.table=FMFTable(name="Test", symbol="\tau")
        self.table.add_data_definition({'Bias Voltage':'U_1 [mV]'})
        self.table.add_data_definition('Acceleration Voltage','U_2(U_1) [kV]')
