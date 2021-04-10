FROM ubuntu:18.04

#########################################
### Python
RUN apt-get update && apt-get -y install git wget build-essential
RUN apt-get install -y python3 python3-pip
RUN ln -s python3 /usr/bin/python
RUN ln -s pip3 /usr/bin/pip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-tk

#########################################
### Numpy
RUN pip install numpy

#########################################
### Make sure we have python3 and a working locale
RUN rm /usr/bin/python && ln -s python3 /usr/bin/python && rm /usr/bin/pip && ln -s pip3 /usr/bin/pip
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
RUN apt-get install -y locales && locale-gen en_US.UTF-8

# python packages
RUN pip install spikeextractors==0.9.6 spiketoolkit==0.7.5 spikesorters==0.4.4
RUN pip install --upgrade kachery==0.6.7

# install extractor dependencies (TODO fix versions)
RUN pip install h5py
RUN pip install scipy
RUN pip install pyintan
RUN pip install pyopenephys
RUN pip install neo
RUN pip install MEArec
RUN pip install pynwb
RUN pip install lxml
RUN pip install nixio
RUN pip install shybrid pyyaml
RUN pip install nixio
RUN pip install mtscomp
