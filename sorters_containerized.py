from pathlib import Path
import random
import hither
import time
import spikesorters as ss
import spikeextractors as se

container_folder = Path(__file__).parent / "containers"


@hither.function('klusta', '0.1.0', container='docker://alejoe91/klusta-0.1.0')
def klusta(
        recording_json, **kwargs
):
    recording = se.load_extractor_from_json(recording_json)
    # run sorter
    t_start = time.time()
    sorting = ss.run_klusta(recording, **kwargs)
    t_stop = time.time()
    print('KLUSTA run time {:.3f}s'.format(t_stop - t_start))
    output_folder = Path(kwargs['output_folder'])
    sorting.dump_to_json(output_folder / 'sorting_output.json')


@hither.function('herdingspikes', '0.1.0', container='docker://alejoe91/herdingspikes-0.1.0')
def herdingspikes(
        recording_json, **kwargs
):
    recording = se.load_extractor_from_json(recording_json)
    # run sorter
    t_start = time.time()
    sorting = ss.run_herdingspikes(recording, **kwargs)
    t_stop = time.time()
    print('HERDINGSPIKES run time {:.3f}s'.format(t_stop - t_start))
    output_folder = Path(kwargs['output_folder'])
    sorting.dump_to_json(output_folder / 'sorting_output.json')


@hither.function('mountainsort4', '0.1.0', container='docker://alejoe91/mountainsort4-0.1.0')
def mountainsort4(
        recording_json, **kwargs
):
    recording = se.load_extractor_from_json(recording_json)
    # run sorter
    t_start = time.time()
    sorting = ss.run_mountainsort4(recording, **kwargs)
    t_stop = time.time()
    print('MS4 run time {:.3f}s'.format(t_stop - t_start))
    output_folder = Path(kwargs['output_folder'])
    sorting.dump_to_json(output_folder / 'sorting_output.json')


def run_sorter(_sorter_function, recording, output_folder, delete_output_folder=False,
               grouping_property=None, parallel=False, verbose=False, raise_error=True, n_jobs=-1,
               joblib_backend='loky',
               **params):
    output_folder = Path(output_folder)
    recording_json = output_folder / "recording_input.json"
    sorting_json = output_folder / "sorting_output.json"

    # dumo recording
    recording.dump_to_json(output_folder / "recording_input.json")

    sorting_job = _sorter_function.run(recording_json=recording_json, output_folder=output_folder,
                                       delete_output_folder=delete_output_folder,
                                       grouping_property=grouping_property, parallel=parallel,
                                       verbose=verbose, raise_error=raise_error, n_jobs=n_jobs,
                                       joblib_backend=joblib_backend,
                                       **params)
    sorting_job.wait()
    sorting = se.load_extractor_from_json(sorting_json)

    return sorting


def run_klusta(*args, **kwargs):
    sorting = run_sorter(klusta, *args, **kwargs)
    return sorting


def run_herdingspikes(*args, **kwargs):
    sorting = run_sorter(herdingspikes, *args, **kwargs)
    return sorting


def run_mountainsort4(*args, **kwargs):
    sorting = run_sorter(mountainsort4, *args, **kwargs)
    return sorting


def test_klusta(output_folder):
    rec, _ = se.example_datasets.toy_example(dumpable=True)

    sorting = run_klusta(rec, output_folder=output_folder)

    print(f"Kusta found #{len(sorting.get_unit_ids())} units")

    return sorting


def test_herdingspikes(output_folder):
    rec, _ = se.example_datasets.toy_example(dumpable=True)

    sorting = run_herdingspikes(rec, output_folder=output_folder)

    print(f"HS2 found #{len(sorting.get_unit_ids())} units")

    return sorting


def test_ms4(output_folder):
    rec, _ = se.example_datasets.toy_example(dumpable=True)

    sorting = run_mountainsort4(rec, output_folder=output_folder)

    print(f"MS4 found #{len(sorting.get_unit_ids())} units")

    return sorting
