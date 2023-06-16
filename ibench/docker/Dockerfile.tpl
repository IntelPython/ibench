# Copyright (C) 2016 Intel Corporation
#
# SPDX-License-Identifier: MIT

{% if os_name == "centos" %}

{% elif os_name == "ubuntu" %}
FROM ubuntu:16.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt install -y \
    libatlas3-base \
    libblas3 \
    liblapack3 \
    libopenblas-base \
    numactl \
    python \
    python-pip \
    unzip \
    wget \
    && pip install --upgrade pip
{% endif %}

ARG MINICONDA_PACKAGE=Miniconda3-4.1.11-Linux-x86_64.sh

RUN wget --quiet https://github.com/rscohn2/ibench/archive/master.zip \
    && unzip master.zip \
    && rm master.zip

{% if config == "shared" %}

RUN pip install numpy scipy \
    && pip install -e ibench-master

# create all the anaconda installations
RUN wget -q https://repo.continuum.io/miniconda/$MINICONDA_PACKAGE
RUN chmod +x $MINICONDA_PACKAGE
ARG MINICONDA=/miniconda3
RUN ./$MINICONDA_PACKAGE -b -p $MINICONDA
RUN rm $MINICONDA_PACKAGE \
    && $MINICONDA/bin/conda update -y -q conda
ENV ACCEPT_INTEL_PYTHON_EULA=yes
RUN $MINICONDA/bin/conda create -y -q -n idp2017.0.0 -c intel intelpython3_core=2017.0.0
RUN $MINICONDA/envs/idp2017.0.0/bin/pip install -e ibench-master
RUN $MINICONDA/bin/conda create -y -q -n idp2017.0.1 -c intel intelpython3_core=2017.0.1
RUN $MINICONDA/envs/idp2017.0.1/bin/pip install -e ibench-master \
    && $MINICONDA/bin/conda create -y -q -n anaconda scipy \
    && $MINICONDA/envs/anaconda/bin/pip install -e ibench-master

{% else %}

RUN apt-get install -y \
    python3-numpy \
    python3-scipy \
    pip install -e ibench-master

{% if config == "sys_atlas" %}
RUN update-alternatives --set libblas.so.3 /usr/lib/atlas-base/atlas/libblas.so.3 \
    && update-alternatives --set liblapack.so.3 /usr/lib/atlas-base/atlas/liblapack.so.3
{% elif config == "sys_openblas" %}
RUN update-alternatives --set libblas.so.3 /usr/lib/openblas-base/libblas.so.3 \
    && update-alternatives --set liblapack.so.3 /usr/lib/openblas-base/liblapack.so.3
{% elif config == "sys_reference" %}
RUN update-alternatives --set libblas.so.3 /usr/lib/libblas/libblas.so.3 \
    && update-alternatives --set liblapack.so.3 /usr/lib/lapack/liblapack.so.3
{% endif %}
{% endif %}

MAINTAINER Robert Cohn <Robert.S.Cohn@intel.com>
LABEL org.label-schema.build-date="{{build_date}}" \
      org.label-schema.name="IDP Python benchmarking container" \
      org.label-schema.description="Container used for benchmarking scipy stack and related components" \
      org.label-schema.url="https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html" \
      org.label-schema.vcs-ref="{{vcs_ref}}" \
      org.label-schema.vcs-url="https://github.com/rscohn2/IDP-bench-docker" \
      org.label-schema.vendor="Intel" \
      org.label-schema.schema-version="1.0"
