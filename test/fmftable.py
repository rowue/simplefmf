# test to check FMFTable
import simplefmf

table_name = "Test"
table_symbol = "\tau"

o = simplefmf.FMFTable(name=table_name, symbol=table_symbol)

if (o.get_name() != table_name):
    raise ValueError, "Comparsion of table_name failed"

if (o.get_symbol() != table_symbol):
    raise ValueError, "Comparsion of table_symbol failed"

o.add_data_definition({'u1':'mV'})
o.add_data_definition({'u2(u1)':'kV'})

print o.get_data_definitions()
print o.get_data_index()

o.set_data_definitions([{'u1': 'kV'}, {'u2(u1)': 'mV'}])
print o.get_data_definitions()
print o.get_data_index()

o.set_data([(1,2,3),(1,2,3), (3,2,1)])
print o.get_data()
if o.verify_consistency():
    raise TypeError, "Fuck"
o.set_data([(1,2,3),(1,2)])
print o.get_data()
if o.verify_consistency():
    raise TypeError, "Fuck"
o.set_data([(1,2,3),(3,2,1)])
print o.get_data()
if not o.verify_consistency():
    raise TypeError, "Fuck"
b = o.get_col_names()
print b
print b[0]
print o.get_data_index()
print o.get_data_by_col_name(b[0])
c = o.get_data_by_row()
while c != None:
    print c
    c = o.get_data_by_row()
print o.get_definition_by_name(b[0])
