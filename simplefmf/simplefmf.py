class FMFTable(object):


    """Class for managing the individual data-tables.

    """
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
        self._data_index = {}       #   Index to definitions excl. comments.
        self._col_index = {}        #   Mapping definitions to rows
        self._col_count = 0
        self._row_count = 0
        self.name = name
        self.symbol = symbol

    def _clear_index(self):
        """Clear definition index."""
        if len(self._data_index) != 0:
            self._data_index = {}
            self._col_index = {}

    def _rebuild_index(self):
        """Rebuild definition index.

           It may lend to problems if the definitions where
           not simple strings but more complicated types
           of objects.

        """
        self._clear_index()
        counter = 0
        for value, key in enumerate(self._data_definition):
            if isinstance(key, dict):
                key_list = key.keys()
                self._data_index[key_list[0]] = value
                self._col_index[key_list[0]] = counter
                counter += 1

    def _set_data_definitions(self, definition):
        """Set the data definition.
        
           This method is intended to set up the
           whole set of definitions in an bunch.

        """
        self._data_definition = definition
        self._rebuild_index()

    data_definitions = property(lambda self: self._data_definition,
                                _set_data_definitions)

    def add_data_definition(self, value, description=None):
        """Add an data definition.
        
           This method is intended to declare
           definitions with iterative calls.

           You can call this method either direct with
           an dict (name:definition) or supply two
           strings where the first is the name, the
           second is the definition ("U1", "mV").
           You may even let the description blank,
           which would be charged as comment.

        """
        if description is not None:
            tmp_val = {}
            tmp_val[value] = description
            value = tmp_val
        if isinstance(value, dict):     # Not a comment
            key_list = value.keys()
            self._col_index[key_list[0]] = len(self._data_index)
            self._data_index[key_list[0]] = len(self._data_definition)
        self._data_definition.append(value)

    def add_data_column(self, column):
        """Add a complete column of data."""
        if self._col_count >= len(self._data_index):
            raise RuntimeError("Too many columns. "
                + " According to data definitions there should be "
                + str(len(self._data_index)) + " columns instead "
                + " of " + str(self._col_count) + ".")
        else:
            self.data.append(column)
            self._col_count += 1

    def add_data_row(self, row):
        """Add a row of data."""
        if len(row) != len(self._data_index):
            raise RuntimeError("Too many columns in row. "
                + " According to data definitions there should be "
                + str(len(self._data_index)) + " columns per row instead "
                + " of " + str(self._col_count) + ".")
        else:
            if len(self.data) == 0:
                for  i in xrange(len(row)):
                    self.data.append([])
            for  i in xrange(len(row)):
                self.data[i].append(row[i])

    data_row = property(None, add_data_row)
        
    def verify_consistency(self):
        """Verifys if the data structure is consistent.

           The number of columns have to be equal to the number
           of definitions and the number of rows has to be
           the same on all columns.

           Return None if there is no data to verify.

        """
        if len(self._data_index) != len(self.data):
            return False
        else:
            if len(self.data) > 0:
                testcount = len(self.data[0])
                for i in xrange(1, len(self.data)):
                    testcolumn = self.data[i]
                    if len(testcolumn) != testcount:
                        return False
                return True
            else:
                return None

    def write_table_entry (self, filehandle):
        """Write table entry in table definitions on filehandle."""
        pattern = "%s: %s\n"
        if self.name is not None and self.symbol is not None:
            filehandle.write(pattern % (self.name, self.symbol))

    def write_table_definition (self, filehandle, comment,
                                comments=True):
        """Write the table definitions to filehandle.
        
           Comments will be suppressed if comments is set to false.

        """
        pattern = "%s: %s\n"
        if self.symbol is not None:
            filehandle.write(pattern % ("[*data definitions", 
                            self.symbol + "]"))
        else:
            filehandle.write("[*data definitions]\n")
        if comments:
            commpattern = "%s %s\n"
        for i in self._data_definition:
            if isinstance(i, dict):
                keylist = i.keys()
                key = keylist[0]
                filehandle.write(pattern % (key, i[key]))
            elif comments:
                filehandle.write(commpattern % (comment, repr(i)))

    def write_table_data (self, filehandle, delimeter):
        """Write table data to filehandle."""
        pattern = "%s: %s\n"
        joinpattern = delimeter
        if self.symbol is not None:
            filehandle.write(pattern % ("[*data", self.symbol + "]"))
        else:
            filehandle.write("[*data]\n")
        if delimeter.lower() == "semicolon":
            joinpattern = ";"
        elif delimeter.lower() == "whitespace":
            joinpattern = "\t"  #   do st nasty
        for i in range(len(self.data[0])):
            tmpbuf = []
            for j in range(len(self.data)):
                a = self.data[j]           # This line sucks
                tmpbuf.append(repr(a[i]))   
            outbuf = joinpattern.join(tmpbuf)
            if delimeter.lower() == "whitespace":
                outbuf.expandtabs(4)
            filehandle.write(outbuf + "\n")
                
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
        self.reference = {}
        self.subreference = None
        self.subreferences = {}
        self.tables = []
        self.tableref_symbol = {}
        self.tableref_name = {}
        self.section_order = []
        self.reference_order = {}
        self._base_reference_order = [ 'title', 'creator', 'created', 'place']
        self._estimate_creation_date(created)   # self.reference[created]
        self._estimate_creator(creator)         # self.reference[creator]
        self._estimate_charset()                # self.charset
        self.reference['title'] = title
        if place is None:
            place = "Earth, Universe"
        self.reference['place'] = place
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
                created = "1970-01-01 00:00:00+00:00"
        else:
            created = created
        self.reference['created'] = created

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
        self.reference['creator'] = creator

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
        self.subreference = name
        self.subreferences[name] = {}
        self.section_order.append(name)
        self.reference_order[name] = []

    def add_reference_entry (self, name, data):
        """Add reference entry.
        
           Use in conjunction with "add_reference_section".

        """
        if self.subreference is None:
            refname = self.reference
            self._base_reference_order.append(name)
        else:
            refname = self.subreferences[self.subreference]
            self.reference_order[self.subreference].append(name)
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
            if self.subreference is None:
                refname = self.reference
                self._base_reference_order.append(name)
            else:
                refname = self.subreferences[self.subreference]
                self.reference_order[self.subreference].append(name)
        else:
            if not self.subreferences.has_key(subsection):
                self.subreferences[subsection] = {}
                self.section_order.append(subsection)
            refname = self.subreferences[subsection]
            self.reference_order[subsection].append(name)
        refname[name] = data    # perhaps we should change to an list here

    def build_table_index (self):
        """This method rebuilds the table indexes."""
        self.tableref_symbol = {}
        self.tableref_name = {}
        number_of_tables = len(self.tables)

        for i in range(number_of_tables):
            table = self.tables[i]
            if number_of_tables > 1 \
                and (table.name() is None or table.symbol() is None):
                self.tableref_symbol = {}
                self.tableref_name = {}
                raise ValueError, "Multiple tables must have names and symbols."
            self.tableref_symbol[table.symbol] = i
            self.tableref_name[table.name] = i

    #
    #   Methods for reading and writing
    #

    def write_header (self, filehandle):
        """This method writes the headerline."""
        pattern = "%s -*- %s; %s; %s -*-\n"
        deli = repr(self.delimeter)
        filehandle.write(pattern % (self.comment,
            "fmf-version: " + repr(self.fmfversion),
            "coding: " + self.charset,
            "delimeter: " + deli.replace("'","")))
        pattern = "%s %s\n"
        filehandle.write(pattern % (self.comment,
            "Full-Metadata Format as described in " +
                        "http://arxiv.org/abs/0904.1299"))
        filehandle.write(pattern % (self.comment,
            "written by simplefmf " + str(self.version) + " (python)"))

    def write_reference (self, filehandle, section, name=None):
        """This method writes the reference sections."""
        if name is None:    #   main section
            filehandle.write("[*reference]\n")
            liste = self._base_reference_order
        else:
            pattern = "[%s]\n"
            filehandle.write(pattern % name)
            liste = self.reference_order[name]
        pattern = "%s: %s\n"
        for key in liste:
            if isinstance(section[key], basestring):
                filehandle.write(pattern % (key, section[key]))
            elif isinstance(section[key], dict) \
                or isinstance(section[key], list):
                seperator=", "
                filehandle.write(pattern % key)
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
                filehandle.write(pattern % (key, seperator.join(holder)))
            else:
                filehandle.write(pattern % (key, repr(section[key])))

    def write_to_file (self, filename):
        """This method writes the data in an (FMF-)file."""
        status = False
        # TODO: verify some boundary conditions before writing
        filehandle = open(filename, 'w')
        if filehandle is not None:  #   TODO: exception handling
            self.write_header(filehandle)
            self.write_reference(filehandle, self.reference)
            for name in self.section_order:
                self.write_reference(filehandle,
                        self.subreferences[name], name)
            tmp_table = self.tables[0]
            if len(self.tables) > 1 or tmp_table.get_symbol() != None:
                filehandle.write("[*table definitions]\n")
                for tmp_table in self.tables:
                    tmp_table.write_table_entry(filehandle)
            for tmp_table in self.tables:
                tmp_table.write_table_definition (filehandle, self.comment)
                tmp_table.write_table_data(filehandle, self.delimeter)
            filehandle.close()
            status = True
        return status