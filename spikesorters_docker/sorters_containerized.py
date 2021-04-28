from pathlib import Path
import hither2 as hither
import time
import numpy as np
import spikesorters as ss
import spikeextractors as se
from .default_docker_images import default_docker_images


class SpikeSortingDockerHook(hither.RuntimeHook):
    def __init__(self):
        super().__init__()

    def precontainer(self, context: hither.PreContainerContext):
        # this gets run outside the container before the run, and we have a chance to mutate the kwargs,
        # add bind mounts, and set the image
        input_directory = context.kwargs['input_directory']
        output_directory = context.kwargs['output_directory']

        context.add_bind_mount(hither.BindMount(source=input_directory,
                                                target='/input', read_only=True))
        context.add_bind_mount(hither.BindMount(source=output_directory,
                                                target='/output', read_only=False))
        context.image = default_docker_images[context.kwargs['sorter_name']]
        context.kwargs['output_directory'] = '/output'
        context.kwargs['input_directory'] = '/input'


@hither.function('run_sorter_docker_with_container', '0.1.0', image=True, runtime_hooks=[SpikeSortingDockerHook()])
def run_sorter_docker_with_container(
        recording_dict, sorter_name, input_directory, output_directory, **kwargs
):
    recording = se.load_extractor_from_dict(recording_dict)
    # run sorter
    kwargs["output_folder"] = f"{output_directory}/working"
    t_start = time.time()
    # set output folder within the container
    sorting = ss.run_sorter(sorter_name, recording, **kwargs)
    t_stop = time.time()
    print(f'{sorter_name} run time {np.round(t_stop - t_start)}s')
    # save sorting to npz
    se.NpzSortingExtractor.write_sorting(sorting, f"{output_directory}/sorting_docker.npz")


def run_sorter_docker(sorter_name, recording, output_folder, delete_output_folder=False,
                      grouping_property=None, parallel=False, verbose=False, raise_error=True, n_jobs=-1,
                      joblib_backend='loky', use_docker=True, container=None,
                      **params):
    if use_docker:
        # if container is None:
        #     assert sorter_name in default_docker_images, f"Default docker image for {sorter_name} not found"
        #     docker_image = default_docker_images[sorter_name]
        #
        # print(f"Running in docker image {docker_image.get_name()}")
        output_folder = Path(output_folder).absolute()
        output_folder.mkdir(exist_ok=True, parents=True)

        # dump recording with relative file paths to docker container /input folder
        dump_dict_container, input_directory = modify_input_folder(recording.dump_to_dict(), '/input')

        with hither.Config(use_container=False, show_console=True):
            kwargs = dict(recording_dict=dump_dict_container,
                          sorter_name=sorter_name,
                          output_folder=str(output_folder),
                          delete_output_folder=False,
                          grouping_property=grouping_property, parallel=parallel,
                          verbose=verbose, raise_error=raise_error, n_jobs=n_jobs,
                          joblib_backend=joblib_backend)
            kwargs.update(params)
            kwargs.update({'input_directory': str(input_directory), 'output_directory': str(output_folder)})

            sorting_job = hither.Job(run_sorter_docker_with_container, kwargs)
            sorting_job.wait()
        sorting = se.NpzSortingExtractor(output_folder / "sorting_docker.npz")
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
    return run_sorter_docker("klusta", *args, **kwargs)


def run_herdingspikes(*args, **kwargs):
    return run_sorter_docker("herdingspikes", *args, **kwargs)


def run_mountainsort4(*args, **kwargs):
    return run_sorter_docker("mountainsort4", *args, **kwargs)


def run_spykingcircus(*args, **kwargs):
    return run_sorter_docker("spykingcircus", *args, **kwargs)


def modify_input_folder(dump_dict, input_folder="/input"):
    if "kwargs" in dump_dict.keys():
        dcopy_kwargs, folder_to_mount = modify_input_folder(dump_dict["kwargs"])
        dump_dict["kwargs"] = dcopy_kwargs
        return dump_dict, folder_to_mount
    else:
        if "file_path" in dump_dict:
            file_path = Path(dump_dict["file_path"])
            folder_to_mount = file_path.parent
            file_relative = file_path.relative_to(folder_to_mount)
            dump_dict["file_path"] = f"{input_folder}/{str(file_relative)}"
            return dump_dict, folder_to_mount
        elif "folder_path" in dump_dict:
            folder_path = Path(dump_dict["folder_path"])
            folder_to_mount = folder_path.parent
            folder_relative = folder_path.relative_to(folder_to_mount)
            dump_dict["folder_path"] = f"{input_folder}/{str(folder_relative)}"
            return dump_dict, folder_to_mount
        elif "file_or_folder_path" in dump_dict:
            file_or_folder_path = Path(dump_dict["file_or_folder_path"])
            folder_to_mount = file_or_folder_path.parent
            file_or_folder_relative = file_or_folder_path.relative_to(folder_to_mount)
            dump_dict["file_or_folder_path"] = f"{input_folder}/{str(file_or_folder_relative)}"
            return dump_dict, folder_to_mount
        else:
            raise Exception


def return_local_data_folder(recording, input_folder='/input'):
    """
    Modifies recording dictionary so that the file_path, folder_path, or file_or_folder path is relative to the
    'input_folder'

    Parameters
    ----------
    recording: se.RecordingExtractor
    input_folder: str

    Returns
    -------
    dump_dict: dict

    """
    assert recording.is_dumpable
    from copy import deepcopy

    d = recording.dump_to_dict()
    dcopy = deepcopy(d)

    return modify_input_folder(dcopy, input_folder)

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
