# Spikesorters in Docker

Containerized version of spikesorters package. The containerization approach uses 
[hither](https://github.com/flatironinstitute/hither) and it's inspired by the 
[SpikeForest](https://github.com/flatironinstitute/spikeforest2) project

This repo is a test repo before adding this functionality to 
[spikesorters](https://github.com/SpikeInterface/spikesorters) and 
[spikeinterface1.0](https://github.com/SpikeInterface/spikeinterface/tree/big_refactoring).

### Install

```bash
python setup.py install
```

## Basic usage

```python
import spikeextractors as se
import spikesorters_docker as ss

# create a dumpable test example
rec, _ = se.example_datasets.toy_example(dumpable=True)

# run sorter in Docker container
ss.run_klusta(rec, output_folder="klusta_docker", use_docker=True) 

# by default, the following docker images are used
print(ss.default_docker_images)
```
