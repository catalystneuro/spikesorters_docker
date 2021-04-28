import spikeextractors as se
import spikesorters_docker as ssd


rec, _ = se.example_datasets.toy_example(dumpable=True)

output_folder = "ms4_test_docker"

sorting = ssd.run_mountainsort4(rec, output_folder=output_folder)

print(f"MS4 found #{len(sorting.get_unit_ids())} units")

# output_folder = "sc_test_docker"
#
# sorting = ssd.run_spykingcircus(rec, output_folder=output_folder)
#
# print(f"SC found #{len(sorting.get_unit_ids())} units")
