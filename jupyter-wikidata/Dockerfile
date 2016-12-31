FROM ubuntu:16.04
MAINTAINER Pawel Cejrowski <pcejrowski@gmail.com

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
  && rm -rf /var/lib/apt/lists/*

RUN curl -qsSLkO \
    https://repo.continuum.io/miniconda/Miniconda-latest-Linux-`uname -p`.sh \
  && bash Miniconda-latest-Linux-`uname -p`.sh -b \
  && rm Miniconda-latest-Linux-`uname -p`.sh

ENV PATH=/root/miniconda2/bin:$PATH

RUN conda install -y \
    h5py \
    pandas

RUN conda install -y \
    jupyter \
    matplotlib \
    seaborn

WORKDIR /notebooks
ADD ./matrix /notebooks/data
EXPOSE 8888
CMD jupyter notebook --no-browser --ip=0.0.0.0
