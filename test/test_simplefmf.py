# -*- coding: utf-8; -*-

# Copyright (c) 2010-2011, Rectorate of the University of Freiburg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the Freiburg Materials Research Center,
#   University of Freiburg nor the names of its contributors may be used to
#   endorse or promote products derived from this software without specific
#   prior written permission.
#
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__id__ = "$Id: __init__.py 77 2011-05-10 09:14:35Z rowue $"
__author__ = "$Author: rowue $"
__version__ = "$Revision: 77 $"

import nose
import re
from nose.tools import assert_almost_equal, ok_, eq_, assert_true, \
        assert_false
# test to check FMFTable
from simplefmf import SimpleFMF, FMFTable, FMFDataDefinition

class TestSimpleFMFDefault():
    def setUp(self):
        self.simple_fmf=SimpleFMF()

    def test_default_title(self):
        eq_(self.simple_fmf._reference['title'], "-")

    def test_default_place(self):
        eq_(self.simple_fmf._reference['place'], "Earth, Universe")

    def test_default_reference_section(self):
        list=self.simple_fmf.reference_line(self.simple_fmf._reference)
        test_list=[
                "[*reference]",
                "title: -",
                "creator: " + self.simple_fmf._reference['creator'],
                "created: " + self.simple_fmf._reference['created'],
                "place: Earth, Universe"]
        eq_(list, test_list)

    def test_default_header(self):
        header_vals=re.compile(";\s-\*-\s(.*)\s-\*-")
        list=self.simple_fmf.headerline()
        
        # coding=re.compile("; fmf-version: \d\.\d; coding:\s[^;];
        # eq_(list[0], "[*reference]")
        # eq_(list[1], "Full-Metadata Format as described in " +
        #              "http://arxiv.org/abs/0904.1299")
        # eq_(list[2], "place: Earth, Universe")

class TestSimpleFMF():
    def setUp(self):
        self.simple_fmf=SimpleFMF()

    def test_default_title(self):
        eq_(self.simple_fmf._reference['title'], "-")

    def test_default_place(self):
        eq_(self.simple_fmf._reference['place'], "Earth, Universe")

    def test_default_reference_section(self):
        list=self.simple_fmf.reference_line(self.simple_fmf._reference)
        eq_(list[0], "[*reference]")
        eq_(list[1], "title: -")
        eq_(list[4], "place: Earth, Universe")

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
