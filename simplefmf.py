class FMFTable:
    """Class for managing the individual data-tables.

    """

    def __init__(self,
            name=None,
            symbol=None):

        # Structure as follows
        # name and letter holds the name an letters of the table
        # this is not necessary if you use one table but it's needed
        # if you use more of them
        # 
        # data_definition holds a collection of the definitions
        # of the individual data rows
        #
        # data container holds the individual data rows
        #
        # I'm aware that much of the data-row handling is easier
        # with numpy - however using numpy requires numpy as
        # dependency - and one goal of this module is to be as
        # small and "simple" as possible
        #

        self.comment = []
        self.data_definition = []
        self.data = []
        self.data_index = {}
        self._col_count = 0
        self._row_count = 0

        self.set_name(name)
        self.set_symbol(symbol)

    def set_name(self, name):
        """Set's the name of the table."""

        self.name = name
            
    def set_symbol(self, symbol):
        """Set's the symbol of the table.
        
        """

        self.symbol = symbol

    def get_name(self):
        """Returns the name of the table."""

        return self.name

    def get_symbol(self):
        """Returns the symbol of the table."""

        return self.symbol

    def set_data_definitions(self, definition):
        """Set's the data definition.
        
           This method is intended to set up the
           whole set of definitions in an bunch.

        """

        if definition is not None:
            # Maybe more checking here
            self.data_definition = definition
            self.rebuild_index()
        else:
            # Maybe not the right Error
            raise ValueError

    def get_data_definitions(self):
        """Get's the data definition."""

        return self.data_definition

    def add_data_definition(self, value, description=None):
        """Add's an data definition.
        
           This method is intended to decalare
           definitions with iterative calls.

           You can call this method either direct with
           an dict (name:definition) or supply two
           strings where the first is the name, the
           second is the definition ("U1", "mV").

           You may even let the description blank,
           which would provide unusuable results.
        
        """

        if value is not None:
            # Maybe more checking here

            if isinstance(value, dict) and description is None:
                self.data_definition.append(value)
            elif isinstance(value, basestring):
                tmp_val = {}
                tmp_val[value] = description
                self.data_definition.append(tmp_val)
            else: 
                raise TypeError, "Please use dict or string"

            if (len(self.data_index) != 0):
                self.clear_index()
        else:
            # Maybe not the right Error
            raise TypeError, "You should provide some data"

    def set_data(self, data):
        """This method is intended to set all data at once."""

        if data is not None:
            self.data = data
        else:
            # Maybe not the right Error
            raise ValueError

    def add_data_column(self, column):
        """This method is intended to add some data on per column basis."""

        if (column is not None) \
            and (self._col_count < len(self.data_definition)):
            self.data.append(column)
            self._col_count += 1
        else:
            # Maybe not the right Error
            raise ValueError

    def add_data_row(self, row):
        """This method is intended to add some data on per row basis."""

        if row is not None and (len(row) == len(self.data_definition)):
            if (len(self.data) == 0):
                for  i in range(len(row)):
                    self.data.append([])
                       
            for  i in range(len(row)):
                self.data[i].append(row[i])
        else:
            # Maybe not the right Error
            raise TypeError

    def get_data(self):
        """This method is intended to gather all data."""

        return self.data

    def get_data_by_row(self):
        """This method is intended to gather on per row basis."""

        out = []

        if (len(self.data[0]) > self._row_count):
            for i in range(len(self.data)):
                tmp_data = self.data[i]
                out.append(tmp_data[self._row_count])

            self._row_count += 1

            return out
        else:
            return None
        
    def get_data_by_col_num(self, number):
        """This method is intended to gather on per column basis."""

        if number is not None:
            return self.data[number]

    def clear_index(self):
        """This method clears the definition index."""

        if (len(self.data_index) != 0):
            self.data_index = {}

    def rebuild_index(self):
        """This method rebuilds the index of definitions.

           It may lend to problems if the definitions where
           not simple strings but more complicated types
           of objects.

        """

        self.clear_index()
        
        for value, key in enumerate(self.data_definition):
            key_list = key.keys()
            self.data_index[key_list[0]] = value


    def get_data_index(self):
        """This method is intended to get the column index."""

        if (len(self.data_index) == 0):
            self.rebuild_index()

        return self.data_index

    def get_col_names(self):
        """This method is intended to get the column names."""

        out = []

        for value, key in enumerate(self.data_definition):
            key_list = key.keys()
            out.append(key_list[0])

        return out

    def get_definition_by_name(self, name):
        """Returns the definition of an field by its name."""

        if name is not None and self.data_index.has_key(name):
            value = self.data_definition[self.data_index[name]]

            return value[name]
        else:
            return None

    def get_data_by_col_name(self, name):
        """This method is intended to get data by column name."""

        if (len(self.data_index) == 0):
            rebuild_index()

        if name is not None and self.data_index.has_key(name):
            col_num = self.data_index[name]

            return self.data[col_num]
        else:
            raise ValueError

    def verify_consistency(self):
        """This method verifys if the data structure is consistent.

           It verifys if the number of columns is equal to the
           number of column-definitions and if the number of
           rows is the same for all columns.

           It will return None if there is no data to verify.
           True if everything is o.k. False otherwise.
        """

        if (len(self.data_definition) != len(self.data)):
            return False
        else:
            if (len(self.data) > 0):
                testcount = len(self.data[0])

                for i in range(1, len(self.data)):
                    testcolumn = self.data[i]
                    if (len(testcolumn) != testcount):
                        return False
                return True
            else:
                return None

    def write_table_entry (self, filehandle):
        """Writing the table entry in the tables* section."""

        pattern = "%s: %s\n"
        if self.name is not None and self.symbol is not None:
            filehandle.write(pattern % (self.name, self.symbol))

    def write_table_definition (self, filehandle, comment):
        """This method writes the table definitions."""

        pattern = "%s: %s\n"
        if self.symbol is not None:
            filehandle.write(pattern % ("[*data definitions", 
                self.symbol + "]"))
        else:
            filehandle.write("[*data definitions]\n")

        if len(self.comment) != 0:
            for i in self.comment:
                commpattern = "%s %s\n"
                filehandle.write(commpattern % (comment, repr(i)))

        for i in self.data_definition:
            keylist = i.keys()
            key = keylist[0]

            filehandle.write(pattern % (key, i[key]))

    def write_table_data (self, filehandle, delimeter):
        """This method writes the table data."""

        pattern = "%s: %s\n"
        joinpattern = delimeter

        if self.symbol is not None:
            filehandle.write(pattern % ("[*data", 
                self.symbol + "]"))
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
                
class SimpleFMF:
    """Simple implementation of the "Full-Metadata Format".
    
       The Format is desribed in http://arxiv.org/abs/0904.1299.

       "Simple" means there is NO verification of entered units and
       NO searching methods. Furthermore you will get/set some
       memory based structures.

    """

    def __init__(self,
            title='-',
            creator=None,
            place=None,
            created=None):

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
        self.base_reference_order = [
                'title',
                'creator',
                'created',
                'place']

        self.estimate_creation_date(created)    # self.reference[created]
        self.estimate_creator(creator)          # self.reference[creator]
        self.estimate_charset()                 # self.charset

        self.reference['title'] = title

        if (place is None):
            place = "Home"

        self.reference['place'] = place


    # Handling of basic reference data (charset, creator, place, created)

    def estimate_charset (self):
        """Simple method to estimate the used charset from system variables."""
        import locale

        charset = locale.getpreferredencoding()
        self.charset = charset.lower()

    def estimate_creation_date (self, created):
        """Simple method to estimate the creation date if not supplied."""
        if created is None:
            try:
                import time

                created = time.strftime('%Y-%m-%d %H:%M:%S') 
                offset_mask = "%+03d:00"
                if (time.daylight != 0):
                    created += offset_mask % (int(- time.altzone / 3600))
                else:
                    created += offset_mask % (int(- time.timezone / 3600))
            except:
                created = "1970-01-01 00:00:00+00:00"

        else:
            created = created

        self.reference['created'] = created


    def estimate_creator (self, creator):
        """Simple method to estimate the creator if not supplied."""
        if creator is None:
            hostname = self.estimate_hostname()
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
                        creator = "%s <%s@%s>" % (gecos, username, hostname)
                    else:
                        creator = "%s@%s" % (username, hostname)
                except:
                    creator = "%s@%s" % (username, hostname)
            except:
                creator = 'unknown'

        self.reference['creator'] = creator


    def estimate_hostname(self):
        """Simple helper method to estimate the hostname if not supplied.

           This is used for "estimate_creator" to give an E-Mail address.
           
        """

        try:
            import socket
            hostname = socket.getfqdn()
        except:
            hostname = "localhost"

        return hostname

    # Handling of reference data - adding data from outside to memory
    # 
    # The reference data will be held in two sets of dicts
    #
    # a) self.reference - the main section (unnamed)
    # b) self.subreferences an dict of dicts.
    #       Each dict is named by the reference name (setup pe)

    def add_reference_section (self, name):
        """Method to add an reference section. You may either use:
            
           "add_reference_section(Name_of_Section)"
           "add_reference_entry(Name_of_entry, Data)"
           .
           .
           .
           "add_reference_section(Name_of_Section)"

           calls or use "add_subsection_reference_entry".
           The later checks for existence of the occuring section.

        """

        self.subreference = name

        self.subreferences[name] = {}

        self.section_order.append(name)
        self.reference_order[name] = []

    def add_reference_entry (self, name, data):
        """Method to add an reference entry.
        
           May used in conjunction with "add_reference_section"
           for adding subsection entries.

        """

        if (self.subreference is None):
            refname = self.reference
            self.base_reference_order.append(name)
        else:
            refname = self.subreferences[self.subreference]
            self.reference_order[self.subreference].append(name)

        refname[name] = data    # perhaps we should change to an list here

    def add_subsection_reference_entry (self, name, data, subsection=None):
        """Method to directly add an subsection reference entry.
        
           May be used instead of a group of "add_reference_section",
           "add_reference_entry" calls. Can also be used to add an
           reference entry. In the later form this should not be mixed
           with "add_reference_section" calls.

           Will create sections if not existing.

        """

        if (subsection is None):
            if (self.subreference is None):
                refname = self.reference
                self.base_reference_order.append(name)
            else:
                refname = self.subreferences[self.subreference]
                self.reference_order[self.subreference].append(name)
        else:
            if (not self.subreferences.has_key(subsection)):
                self.subreferences[subsection] = {}
                self.section_order.append(subsection)

#        self.reference_order = {}

            refname = self.subreferences[subsection]
            self.reference_order[subsection].append(name)

        refname[name] = data    # perhaps we should change to an list here

    def get_reference_keywords (self, subsection=None):
        """Method to query the keywords from (sub)reference(s).

           If no subsection is supplied the main section will
           be used.

        """

        if (subsection is None):
            reflist = self.reference
        else:
            if self.subreferences.has_key(subsection):
                reflist = self.subreferences[subsection]
            else:
                return None

        return reflist.keys()

#    def set_subsection (self, name=None):
#        """Method (perhaps unused) to set the subsection pointer.
#        
#           In difference to add_subsection the subsection will
#           not be created."""
#
#        if self.subreferences.has_key(name):
#            self.subreference = name
#

    def get_reference_values (self, keyword, subsection=None):
        """Method to query values from reference."""


        if (subsection is None):
            reflist = self.reference
        else:
            if self.subreferences.has_key(subsection):
                reflist = self.subreferences[subsection]
            else:
                return None

        if (not reflist.has_key(keyword)):
            return None

        return reflist[keyword]

    def get_reference_pairs (self, subsection=None):
        """This method is a big sucker.
        
           It returns you an zip with all keywords:value pairs in the
           corresponding (sub)section.

           Keeping subsection unfilled or setting to
           "None" will give you the main reference section.

       """

        if (subsection is None):
            reflist = self.reference
        else:
            if self.subreferences.has_key(subsection):
                reflist = self.subreferences[subsection]
            else:
                return None

        pairs = zip(reflist.keys(), reflist.values()) 

        return pairs

    def get_subsection_names (self):
        """Simply push back the names of the subreferences."""
        return self.subreferences.keys()

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

        if len(self.tables) > 0 \
            and (table.name is None or table.symbol is None):
            raise ValueError, "Multiple tables must have names and symbols."

        if len(self.tableref_symbol) > 0:
            self.tableref_symbol = {}
        if len(self.tableref_name) > 0:
            self.tableref_name = {}

        self.tables.append(table)
        return table

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

    def get_table_by_name (self, name):
        """This method retrieves a table by it's name."""

        if len(self.tableref_name) == 0:
            self.build_table_index()

        if name is not None and self.tableref_name.has_key(name):
            table = self.tables[self.tableref_name[name]]
            return table
        else:
            return None

    def get_table_by_symbol (self, symbol):
        """This method retrieves a table by it's symbol."""

        if len(self.tableref_symbol) == 0:
            self.build_table_index()

        if symbol is not None and self.tableref_symbol.has_key(symbol):
            table = self.tables[self.tableref_symbol[symbol]]
            return table
        else:
            return None

    def get_table_by_number (self, number):
        """This method retrieves a table by it's number."""

        if number is not None:
            table = self.tables[number]
            return table
        else:
            return None
            
    def get_table_names (self):
        """This method returns the names of the tables."""

        if len(self.tableref_name) == 0:
            self.build_table_index()

        return self.tableref_name.keys()

    def get_table_symbols (self):
        """This method returns the symbol of the tables."""

        if len(self.tableref_symbol) == 0:
            self.build_table_index()

        return self.tableref_symbol.keys()

    def get_tables (self):
        """This method returns the tables itself."""

        return self.tables

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
            liste = self.base_reference_order
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
