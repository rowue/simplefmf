# test to check FMFTable
# faselbla
import simplefmf

fmffile = simplefmf.SimpleFMF(
        title="first test of simplefmf",
        place="No place like"
        )

fmffile.add_reference_entry("sample", "655321")
fmffile.add_reference_section("setup")
fmffile.add_reference_entry("beam-energy", "10keV")

table_name = "Hits"
table_symbol = "\hbar"

table = fmffile.add_table(table_name=table_name, table_symbol=table_symbol)

table.add_data_definition("t", "(s)")
table.add_data_definition("h(t)", "(abu)")
table.add_data_row([1,2])
table.add_data_row([3,4])
table.add_data_row([5,6])

fmffile.write_to_file("/tmp/test.fmf")
