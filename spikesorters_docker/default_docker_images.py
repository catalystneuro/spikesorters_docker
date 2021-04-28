import hither2 as hither

default_docker_images = {
    "klusta": 'spikeinterface/klusta-si-0.12:0.2.7',
    "mountainsort4": hither.LocalDockerImage('spikeinterface/mountainsort4-si-0.12:1.0.0'),
    "herdingspikes": 'spikeinterface/herdingspikes-si-0.12:0.3.7',
    "spykingcircus": hither.LocalDockerImage('spikeinterface/spyking-circus-si-0.12:1.0.7')
    # "ironclust": 'docker://spikeinterface/ironclust-cpu:0.1.0',
}
