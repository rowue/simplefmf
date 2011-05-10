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

class FMFDataDefinition(object):
    """Class for managing the individual table-definitions."""

    def __init__(self, name=None, definition=None, mask=None):
        if name is None or definition is None:
            raise ValueError, "You have to specify name and definition."
        self._name=name
        self._definition=definition
        self.mask=mask

    definition_entry = property(lambda self: "%s: %s" % 
                                    (self._name, self._definition))

    def default_mask(self, data):
        """Sets mask to default depending on data-type."""
        fmt = "%s"
        if isinstance(data, float):
            fmt = "%.3e"
        elif isinstance(data, int) and not isinstance(data, bool):
            fmt ="%0d"
        self.mask = fmt


class FMFTable(object):
    """Class for managing the individual data-tables."""

    def __init__(self, name=None, symbol=None):
        # Structure as follows:
        # Name and letter holds the name an letters of the table.
        # This is not necessary if you use one table but it's needed
        # if you use more of them.
        # 
        # _data_definition holds a collection of the definitions
        # of the individual data rows including comments.
        # At this time we use two indexes - one for the 
        # mapping of row to definition and one for mapping
        # definition to data row. The last might vanish if we
        # use a seperate class for definitions.
        #
        # data holds the individual data rows.
        #
        # I'm aware that much of the data-row handling is easier
        # with numpy - however using numpy requires numpy as
        # dependency - and one goal of this module is to be as
        # small and "simple" as possible.
        #
        # Fr 18. Jun 14:20:09 CEST 2010 - rowue
        #

        self._data_definition = []  #   Definitions including comments(!)
        self.data = []
        self._data_index = 0       #   Index to definitions excl. comments.
        self._col_count = 0         #   Number of current columns
        self._row_count = 0
        self.name = name
        self.symbol = symbol

    def _rebuild_index(self):
        """Rebuild definition index.

           It may lend to problems if the definitions where
           not simple strings but more complicated types
           of objects.

        """
        self._data_index = 0
        for definition in (self._data_definition):
            if isinstance(definition, FMFDataDefinition):
                self._data_index += 1

    def _set_data_definitions(self, definitions):
        """Set the data definition.
        
           This method is intended to set up the
           whole set of definitions in an bunch.

        """
        self._data_definition = definitions
        self._rebuild_index()

    data_definitions = property(lambda self: self._data_definition,
                                _set_data_definitions)

    table_entry = property(lambda self: "%s: %s" % (self.name, self.symbol))

    def add_data_definition(self, value, description=None, mask=None):
        """Add an data definition.
        
           This method is intended to declare
           definitions with iterative calls.

           You can call this method either direct with
           a dict (name:definition) or supply two
           strings where the first is the name, the
           second is the definition ("U1", "mV").
           You can also supply a mask to define the way
           how the values in the table are printed.
           If you don't supply it, a predefined default
           will be used (%.3e for floats, %0d for int).

           If you don't supply a definition (in either way),
           the entry will be charged as comment.

        """
        # It might look a little strange to store 
        # two different items in data_definitions
        # comments and FMFDataDefintion.
        # But FMFDataDefinition are distinct from
        # comments so comments should not reside in
        # the FMFDataDefinition object.
        name=None
        if description is not None or isinstance(value, dict):
            self._data_index += 1
            if description is not None:
                data_definition=FMFDataDefinition(name=value, 
                        definition=description)
            else:
                name=value.keys()[0]
                description=value[name]
                data_definition=FMFDataDefinition(name=name, 
                        definition=description)
            if mask is not None:
                data_definition.mask = mask
            self._data_definition.append(data_definition)
        else:
            self._data_definition.append(value)

    def add_data_column(self, column):
        """Add a complete column of data."""
        if self._col_count >= self._data_index:
            raise RuntimeError("Too many columns. "
                + " According to data definitions there should be "
                + str(self._data_index) + " columns instead "
                + " of " + str(self._col_count) + ".")
        else:
            self.data.append(column)
            self._col_count += 1

    def add_data_row(self, row):
        """Add a row of data."""
        if len(row) != self._data_index:
            raise RuntimeError("Too many columns in row. "
                + " According to data definitions there should be "
                + str(self._data_index) + " columns per row instead "
                + " of " + str(len(row)) + ".")
        else:
            if len(self.data) == 0:
                for  i in xrange(len(row)):
                    self.data.append([])
            for  i in xrange(len(row)):
                self.data[i].append(row[i])

    def verify_consistency(self, ref_length=None):
        """Verifys if the data structure is consistent.

           The number of columns have to be equal to the number
           of definitions and the number of rows has to be
           the same on all columns (ref_length). If ref_length
           is omitted the len of the first column will be used.

           Return False if there is no data to verify.

        """
        if self._data_index != len(self.data):
            #   Does number of definitions match number
            #   of columns
            return False
        if len(self.data) > 0:
            if ref_length is None:
                ref_length = len(self.data[0])
            return all([len(c)==ref_length for c in self.data])
        else:
            return False

    def write_table_entry (self, filehandle):
        """Write table entry in table definitions on filehandle."""
        if self.name is None or self.symbol is None:
            raise RuntimeError("You have to define " +
                    "table name and table key if you use " +
                    "more than one tables.")
        else:
            filehandle.write("%s\n" % self.table_entry)

    def table_definition (self, comment, comments=True):
        """Returns an list of strings containing the table definition. 

           This can be written to STDOUT, filehandle or used
           otherwise. Comments will be supressed if
           comments is set to false.

        """
        definition_list = []
        pattern = "%s: %s"
        if self.symbol is not None:
            definition_list.append(pattern % ("[*data definitions", 
                            self.symbol + "]"))
        else:
            definition_list.append("[*data definitions]")
        if comments:
            commpattern = "%s %s"
        for i in self._data_definition:
            if isinstance(i, FMFDataDefinition):
                definition_list.append(i.definition_entry)
            elif comments:
                definition_list.append(commpattern % (comment, i))
        #        definition_list.append(commpattern % (comment, repr(i)))
        return definition_list

    def write_table_definition (self, filehandle, comment,
                                comments=True):
        """Write the table definitions to filehandle.
        
           Comments will be suppressed if comments is set to false.

        """
        definition_list = self.table_definition (comment, comments=True)
        filehandle.write("\n".join(definition_list) + "\n")

    def _build_mask_list(self):
        """Builds the list of masks (None results to defaults)."""
        mask_list=[]
        for i in (self._data_definition):
            if isinstance(i, FMFDataDefinition):
                mask_list.append(i)
        return mask_list

    def table_data (self, delimeter):
        """Returns an list of the data-rows.
        
           Yes, I know: using a list for this sucks a lot.
           But we change it later (and know all about provisorics).
        """
        data_list = []
        pattern = "%s: %s"
        joinpattern = delimeter
        mask_list = self._build_mask_list()
        index_count_row = len(self.data[0])
        index_count_col = len(self.data)

        if self.symbol is not None:
            data_list.append(pattern % ("[*data", self.symbol + "]"))
        else:
            data_list.append("[*data]")
        if delimeter.lower() == "semicolon":
            joinpattern = ";"
        elif delimeter.lower() == "whitespace":
            joinpattern = "\t"  #   do st nasty
        for i in xrange(index_count_row):
            tmpbuf = []
            for j in xrange(index_count_col):
                a = self.data[j][i]           # This line sucks
                if i == 0 and mask_list[j].mask is None:
                    # if this is the first line and the mask is not
                    # defined.
                    mask_list[j].default_mask(a)
                tmpbuf.append(mask_list[j].mask % a)
            outbuf = joinpattern.join(tmpbuf)
            if delimeter.lower() == "whitespace":
                outbuf = outbuf.expandtabs(4)
            data_list.append(outbuf)
        return data_list

    def write_table_data (self, filehandle, delimeter):
        """Write table data to filehandle."""
        data_list = self.table_data (delimeter)
        filehandle.write("\n".join(data_list) + "\n")


class SimpleFMF(object):
    """Simple implementation of the "Full-Metadata Format".
    
       The Format is desribed in http://arxiv.org/abs/0904.1299.
       "Simple" means there is NO verification of entered units and
       NO searching methods.  Furthermore you will worked on
       memory based structures.

    """
    def __init__(self, title='-', creator=None, place=None, created=None):
        self.fmfversion = 1.0
        self.version = 0.1
        self.fmflevel = 0
        self.delimeter = '\t'
        self.comment = ';'
        self._reference = {}
        self._subreference = None
        self._subreferences = {}
        self._tables = []
        self._section_order = []
        self._reference_order = {}
        self._base_reference_order = [ 'title', 'creator', 'created', 'place']
        self._estimate_creation_date(created)   # self.reference[created]
        self._estimate_creator(creator)         # self.reference[creator]
        self._estimate_charset()                # self.charset
        self._reference['title'] = title
        if place is None:
            place = "Earth, Universe"
        self._reference['place'] = place
    # Handling of basic reference data (charset, creator, place, created)

    def _estimate_charset (self):
        """Set used charset from system parameters."""
        import locale
        charset = locale.getpreferredencoding()
        self.charset = charset.lower()

    def _estimate_creation_date (self, created):
        """Set creation date from localtime if not supplied."""
        if created is None:
            try:
                import time
                created = time.strftime('%Y-%m-%d %H:%M:%S') 
                offset_mask = "%+03d:00"
                if time.daylight != 0:
                    created += offset_mask % (int(- time.altzone / 3600))
                else:
                    created += offset_mask % (int(- time.timezone / 3600))
            except:
                #   should be unknown
                created = "1970-01-01 00:00:00+00:00"
        else:
            created = created
        self._reference['created'] = created

    def _estimate_creator (self, creator):
        """Estimate the creator.
        
           Support for setting the E-Mail was dropped.
        """
        if creator is None:
            try:
                import getpass
                username = getpass.getuser()
                try:
                    import pwd
                    gecos = pwd.getpwnam(username).pw_gecos
                    gecos = gecos.replace(",","")
                    hasalpha = False
                    for letter in gecos:
                        if letter.isalpha():
                            hasalpha = True
                    if hasalpha:
                        creator = "%s" % (gecos)
                    else:
                        creator = "%s" % (username)
                except:
                    creator = "%s" % (username)
            except:
                creator = 'unknown'
        self._reference['creator'] = creator

    # Handling of reference data - adding data from outside to memory
    # 
    # The reference data will be held in two sets of dicts
    #
    # a) self.reference - the main section (unnamed)
    # b) self.subreferences an dict of dicts.
    #       Each dict is named by the reference name (setup pe)

    def add_reference_section (self, name):
        """Add an reference section. You may either use:
            
           "add_reference_section(Name_of_Section)"
           "add_reference_entry(Name_of_entry, Data)"
           .
           .
           .
           "add_reference_section(Name_of_Section)"

           or use "add_subsection_reference_entry".
           The later checks for existence of the section.

        """
        self._subreference = name
        self._subreferences[name] = {}
        self._section_order.append(name)
        self._reference_order[name] = []

    def add_reference_entry (self, name, data):
        """Add reference entry.
        
           Use in conjunction with "add_reference_section".

        """
        if self._subreference is None:
            refname = self._reference
            self._base_reference_order.append(name)
        else:
            refname = self._subreferences[self._subreference]
            self._reference_order[self._subreference].append(name)
        refname[name] = data    # perhaps we should change to an list here

    def add_subsection_reference_entry (self, name, data, subsection=None):
        """Add an subsection reference entry.
        
           May be used instead of a group of "add_reference_section",
           "add_reference_entry" calls. Can also be used to add an
           reference entry. In the later form this should not be mixed
           with "add_reference_section" calls.

           Will create sections if not existing.

        """
        if subsection is None:
            if self._subreference is None:
                refname = self._reference
                self._base_reference_order.append(name)
            else:
                refname = self._subreferences[self._subreference]
                self._reference_order[self._subreference].append(name)
        else:
            if not self._subreferences.has_key(subsection):
                self._subreferences[subsection] = {}
                self._section_order.append(subsection)
            refname = self._subreferences[subsection]
            self._reference_order[subsection].append(name)
        refname[name] = data    # perhaps we should change to an list here

    def add_table (self, table=None, table_name=None, table_symbol=None):
        """This method appends an table to the dataset.

           If you supply an table object (simplefmf.FMFTable) this
           object will get appended. If you supply nothing an
           new object will be created.

           As return value you will get the table object.

        """
        if table is None:
            table = FMFTable(name=table_name, symbol=table_symbol)
        elif not isinstance(table, simplefmf.FMFTable):
            raise TypeError, "Please supply simplefmf.FMFTable or nothing."
        if len(self._tables) > 0 \
            and (table.name is None or table.symbol is None):
            raise ValueError, "Multiple tables must have names and symbols."
        self._tables.append(table)
        return table

    def headerline (self):
        """Returns an list of strings containig the header-lines."""
        header_list = []
        pattern = "%s -*- %s; %s; %s -*-"
        deli = repr(self.delimeter)
        header_list.append(pattern % (self.comment,
            "fmf-version: " + repr(self.fmfversion),
            "coding: " + self.charset,
            "delimeter: " + deli.replace("'","")))

        pattern = "%s %s"
        header_list.append(pattern % (self.comment,
            "Full-Metadata Format as described in " +
                        "http://arxiv.org/abs/0904.1299"))
        header_list.append(pattern % (self.comment,
            "written by simplefmf " + str(self.version) + " (python)"))
        return header_list

    def write_header (self, filehandle):
        """This method writes the headerline."""
        header_list = self.headerline()
        filehandle.write("\n".join(header_list) + "\n")

    def reference_line (self, section, name=None):
        """Return a list with the section-selected meta-data."""
        meta_list = []
        if name is None:    #   main section
            meta_list.append("[*reference]")
            liste = self._base_reference_order
        else:
            pattern = "[%s]"
            meta_list.append(pattern % name)
            liste = self._reference_order[name]
        pattern = "%s: %s"
        for key in liste:
            if isinstance(section[key], basestring):
                meta_list.append(pattern % (key, section[key]))
            elif isinstance(section[key], dict) \
                or isinstance(section[key], list):
                seperator=", "
                meta_list.append(pattern % key)
                holder = []
                if isinstance(section[key], dict):
                    tmp_pattern = "%s = %s"
                    tmp_dict = section[key]
                    for i in tmp_dict.keys:
                        holder.append(tmp_pattern % (repr(i),
                                    repr(tmp_dict[i])))
                else:
                    for i in section[key]:
                        holder.append(repr(i))
                meta_list.append(pattern % (key, seperator.join(holder)))
            else:
                meta_list.append(pattern % (key, repr(section[key])))
        return meta_list

    def write_reference (self, filehandle, section, name=None):
        """This method writes the reference sections."""
        meta_list = self.reference_line(section, name)
        filehandle.write("\n".join(meta_list) + "\n")

    def write_to_file (self, filename):
        """This method writes the data in an (FMF-)file."""
        status = False
        # TODO: verify some boundary conditions before writing
        filehandle = open(filename, 'w')
        if filehandle is not None:  #   TODO: exception handling
            self.write_header(filehandle)
            self.write_reference(filehandle, self._reference)
            for name in self._section_order:
                self.write_reference(filehandle,
                        self._subreferences[name], name)
            tmp_table = self._tables[0]
            if len(self._tables) > 1 or tmp_table.symbol != None:
                filehandle.write("[*table definitions]\n")
                for tmp_table in self._tables:
                    tmp_table.write_table_entry(filehandle)
            for tmp_table in self._tables:
                tmp_table.write_table_definition (filehandle, self.comment)
                tmp_table.write_table_data(filehandle, self.delimeter)
            filehandle.close()
            status = True
        return status
