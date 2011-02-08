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

    def test_data_definition_types(self):
        data_list = self.table.data_definitions
        assert_true(isinstance(data_list[0], FMFDataDefinition))
        assert_true(isinstance(data_list[1], FMFDataDefinition))
        assert_false(isinstance(data_list[2], FMFDataDefinition))
        assert_true(isinstance(data_list[2], str))

    def test_data_definition_out(self):
        data_list = self.table.table_definition(";")
        eq_(data_list[0], "[*data definitions: \tau]")
        eq_(data_list[1], "Bias Voltage: U_1 [mV]")
        eq_(data_list[2], "Acceleration Voltage: U_2(U_1) [kV]")
        eq_(data_list[3], "; some stupid comment")

    def test_data_definition_set(self):
        a=[]
        a.append(FMFDataDefinition(name="Bias Voltage", definition="U_1 [mV]"))
        a.append(FMFDataDefinition(name="Beam Current", 
            definition="I_B(U_1) [mA]"))
        self.table.data_definitions = a
        data_list = self.table.data_definitions
        assert_true(isinstance(data_list[0], FMFDataDefinition))
        assert_true(isinstance(data_list[1], FMFDataDefinition))
        data_list = self.table.table_definition(";")
        eq_(data_list[0], "[*data definitions: \tau]")
        eq_(data_list[1], "Bias Voltage: U_1 [mV]")
        eq_(data_list[2], "Beam Current: I_B(U_1) [mA]")

    def test_data_table_mask_auto(self):
        a=[]
        a.append(FMFDataDefinition(name="Measuring Point", 
            definition="n"))
        a.append(FMFDataDefinition(name="Bias Voltage", 
            definition="U_1(n) [mV]"))
        a.append(FMFDataDefinition(name="Shutter", 
            definition="s(n)"))
        a.append(FMFDataDefinition(name="Direction", 
            definition="d(n)"))
        self.table.data_definitions = a
        self.table.data=[
                (0,1),
                (0.1, 1.4568e-10),
                (True, False),
                ("North", "South")]
        data_list = self.table.table_data("\t")
        eq_(data_list[0], "[*data: \tau]")
        eq_(data_list[1], '0\t1.000e-01\tTrue\tNorth')
        eq_(data_list[2], '1\t1.457e-10\tFalse\tSouth')

    def test_data_table_mask_supplied(self):
        a=[]
        a.append(FMFDataDefinition(name="Measuring Point", 
            definition="n", mask="%02d"))
        a.append(FMFDataDefinition(name="Bias Voltage", 
            definition="U_1(n) [mV]", mask="%.1e"))
        a.append(FMFDataDefinition(name="Accelerator Voltage", 
            definition="U_2(n) [V]", mask="%.2f"))
        a.append(FMFDataDefinition(name="Direction", 
            definition="d(n)", mask="\"%s\""))
        self.table.data_definitions = a
        self.table.data=[
                (0,1),
                (0.1, 1.4568e-10),
                (0.1, 0.001),
                ("North", "South")]
        data_list = self.table.table_data("\t")
        eq_(data_list[0], "[*data: \tau]")
        eq_(data_list[1], '00\t1.0e-01\t0.10\t\"North\"')
        eq_(data_list[2], '01\t1.5e-10\t0.00\t\"South\"')

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
