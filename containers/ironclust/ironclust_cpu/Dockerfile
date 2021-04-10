FROM spikeinterface/si-0.12.0-ubuntu20.04:0.1.0

RUN apt-get update && apt-get install -y unzip
RUN apt-get install -y libxt-dev
RUN apt-get install -y curl

RUN mkdir /install_matlab \
    && curl http://ssd.mathworks.com/supportfiles/downloads/R2019b/Release/1/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2019b_Update_1_glnxa64.zip > /install_matlab/MATLAB_Runtime_R2019b_Update_1_glnxa64.zip \
    && cd /install_matlab && unzip MATLAB_Runtime_R2019b_Update_1_glnxa64.zip && ./install -mode silent -agreeToLicense yes && cd / && rm -rf /install_matlab

# See comment above
ENV LD_LIBRARY_PATH /usr/local/MATLAB/MATLAB_Runtime/v97/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v97/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v97/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v97/extern/bin/glnxa64

COPY run_irc.app /run_irc
RUN chmod a+x /run_irc
ENV IRONCLUST_BINARY_PATH=/run_irc
