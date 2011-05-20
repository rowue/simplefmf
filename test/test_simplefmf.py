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
from nose.tools import eq_
# test to check SimpleFMF
from simplefmf import SimpleFMF

class TestSimpleFMFDefault():
    def setUp(self):
        self.simple_fmf=SimpleFMF()

    def test_default_reference_section(self):
        list=self.simple_fmf.reference_line(self.simple_fmf._reference)
        # It might be more interesting to check if creator and created
        # where estimated right
        test_list=[
                "[*reference]",
                "title: -",
                "creator: " + self.simple_fmf._reference['creator'],
                "created: " + self.simple_fmf._reference['created'],
                "place: Earth, Universe"]
        eq_(list, test_list)

        # Perhaps we should also check the header-line if it is right


class TestSimpleFMF_Reference():
    def setUp(self):
        self.simple_fmf=SimpleFMF()

    def test_add_reference_section(self):
        self.simple_fmf.add_reference_section("Setup")
        self.simple_fmf.add_reference_entry("Beam-Energy", "100 MeV")
        list=self.simple_fmf.reference_line(
                self.simple_fmf._subreferences["Setup"],
                "Setup")        #   ugly
        test_list=[
                "[Setup]",
                "Beam-Energy: 100 MeV"
                ]
        eq_(list, test_list)

    def test_add_subsection_reference_entry_base_reference(self):
        self.simple_fmf.add_subsection_reference_entry(
                "contact", "test@test.de")
        list=self.simple_fmf.reference_line(self.simple_fmf._reference)
        test_list=[
                "[*reference]",
                "title: -",
                "creator: " + self.simple_fmf._reference['creator'],
                "created: " + self.simple_fmf._reference['created'],
                "place: Earth, Universe",
                "contact: test@test.de"
                ]
        eq_(list, test_list)

    def test_add_subsection_reference_entry(self):
        self.simple_fmf.add_subsection_reference_entry(
                "temperature", "315.15 K", subsection="Environment")
        list=self.simple_fmf.reference_line(
                self.simple_fmf._subreferences["Environment"],
                "Environment")        #   ugly
        test_list=[
                "[Environment]",
                "temperature: 315.15 K"
                ]
        eq_(list, test_list)
    

    def test_add_subsection_reference_entry_double(self):
        self.simple_fmf.add_subsection_reference_entry(
                "temperature", "42 K", subsection="Heating")
        self.simple_fmf.add_subsection_reference_entry(
                "type", "Flux-Compensator", subsection="Heating")
        list=self.simple_fmf.reference_line(
                self.simple_fmf._subreferences["Heating"],
                "Heating")        #   ugly
        test_list=[
                "[Heating]",
                "temperature: 42 K",
                "type: Flux-Compensator"
                ]
        eq_(list, test_list)

    def test_add_subsection_entry_after(self):
        self.simple_fmf.add_subsection_reference_entry(
                "temperature", "42 K", subsection="Heating")
        self.simple_fmf.add_reference_section("Setup")
        self.simple_fmf.add_reference_entry("Beam-Energy", "100 MeV")
        self.simple_fmf.add_subsection_reference_entry(
                "type", "Flux-Compensator", subsection="Heating")
        list=self.simple_fmf.reference_line(
                self.simple_fmf._subreferences["Heating"],
                "Heating")        #   ugly
        test_list=[
                "[Heating]",
                "temperature: 42 K",
                "type: Flux-Compensator"
                ]
        eq_(list, test_list)
