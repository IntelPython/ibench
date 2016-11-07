{% if os_name == "centos" %}
FROM centos:7
RUN yum install -y \

{% elif os_name == "ubuntu" %}
FROM ubuntu:16.04
RUN apt-get update && apt install -y \
    libatlas3-base \
    libblas3 \
    liblapack3 \
    libopenblas-base \
    numactl \
    python \
    python-pip \
    && pip install --upgrade pip
{% endif %}
WORKDIR /benchdata


{% if config == "pip" %}

RUN pip install numpy scipy

{% else %}

RUN apt-get install -y \
    python3-numpy \
    python3-scipy

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
      org.label-schema.url="https://software.intel.com/en-us/intel-distribution-for-python" \
      org.label-schema.vcs-ref="{{vcs_ref}}" \
      org.label-schema.vcs-url="https://github.com/rscohn2/IDP-bench-docker" \
      org.label-schema.vendor="Intel" \
      org.label-schema.schema-version="1.0"
