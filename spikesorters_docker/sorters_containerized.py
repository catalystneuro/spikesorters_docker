from pathlib import Path
import hither2 as hither
import time
import numpy as np
import spikesorters as ss
import spikeextractors as se
from .default_docker_images import default_docker_images


def run_sorter(sorter_name, recording, output_folder, delete_output_folder=False,
               grouping_property=None, parallel=False, verbose=False, raise_error=True, n_jobs=-1,
               joblib_backend='loky', use_docker=True, container=None,
               **params):
    output_folder = Path(output_folder)
    recording_json = output_folder / "recording_input.json"
    sorting_json = output_folder / "sorting_output.json"

    # dump recording
    recording.dump_to_json(output_folder / "recording_input.json")

    if use_docker:
        if container is None:
            assert sorter_name in default_docker_images, f"Default docker image for {sorter_name} not found"
            docker_image = default_docker_images[sorter_name]

        print(f"Running in docker image {docker_image}")
        # define hither function with container at run time
        @hither.function('run_sorter_docker_with_container', '0.1.0', image=docker_image)
        # @hither.container(docker_image)
        def run_sorter_docker_with_container(
                recording_json, sorter_name, **kwargs
        ):
            recording = se.load_extractor_from_json(recording_json)
            # run sorter
            t_start = time.time()
            sorting = ss.run_sorter(sorter_name, recording, **kwargs)
            t_stop = time.time()
            print(f'{sorter_name} run time {np.round(t_stop - t_start)}s')
            output_folder = Path(kwargs['output_folder'])
            sorting.dump_to_json(output_folder / 'sorting_output.json')

        sorting_job = run_sorter_docker_with_container.run(recording_json=recording_json, sorter_name=sorter_name,
                                                           output_folder=output_folder,
                                                           delete_output_folder=delete_output_folder,
                                                           grouping_property=grouping_property, parallel=parallel,
                                                           verbose=verbose, raise_error=raise_error, n_jobs=n_jobs,
                                                           joblib_backend=joblib_backend,
                                                           **params)
        sorting_job.wait()
        sorting = se.load_extractor_from_json(sorting_json)
    else:
        # standard call
        sorting = ss.run_sorter(sorter_name, recording, output_folder=output_folder,
                                delete_output_folder=delete_output_folder,
                                grouping_property=grouping_property, parallel=parallel,
                                verbose=verbose, raise_error=raise_error, n_jobs=n_jobs,
                                joblib_backend=joblib_backend,
                                **params)

    return sorting


def run_klusta(*args, **kwargs):
    return run_sorter("klusta", *args, **kwargs)


def run_herdingspikes(*args, **kwargs):
    return run_sorter("herdingspikes", *args, **kwargs)


def run_mountainsort4(*args, **kwargs):
    return run_sorter("mountainsort4", *args, **kwargs)


# def run_ironclust(*args, **kwargs):
#     return run_sorter("ironclust", *args, **kwargs)
#
#
# def test_klusta(output_folder=None):
#     if output_folder is None:
#         output_folder = "kl_docker"
#     rec, _ = se.example_datasets.toy_example(dumpable=True)
#
#     sorting = run_klusta(rec, output_folder=output_folder)
#
#     print(f"KL found #{len(sorting.get_unit_ids())} units")
#
#     return sorting
#
#
# def test_herdingspikes(output_folder=None):
#     if output_folder is None:
#         output_folder = "hs_docker"
#     rec, _ = se.example_datasets.toy_example(dumpable=True)
#
#     sorting = run_herdingspikes(rec, output_folder=output_folder)
#
#     print(f"HS2 found #{len(sorting.get_unit_ids())} units")
#
#     return sorting
#
#
# def test_ms4(output_folder=None):
#     if output_folder is None:
#         output_folder = "ms4_docker"
#     rec, _ = se.example_datasets.toy_example(dumpable=True)
#
#     sorting = run_mountainsort4(rec, output_folder=output_folder)
#
#     print(f"MS4 found #{len(sorting.get_unit_ids())} units")
#
#     return sorting
#
#
# def test_ironclust(output_folder=None):
#     if output_folder is None:
#         output_folder = "ic_docker"
#     rec, _ = se.example_datasets.toy_example(dumpable=True)
#
#     sorting = run_ironclust(rec, output_folder=output_folder)
#
#     print(f"IC found #{len(sorting.get_unit_ids())} units")
#
#     return sorting
