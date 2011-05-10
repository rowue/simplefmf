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

__id__ = "$Id$"
__author__ = "$Author$"
__version__ = "$Revision$"

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
