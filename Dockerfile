# Software installation, no database files
# https://github.com/gambit-suite/gambit-tools
FROM mambaorg/micromamba:jammy as app_base

LABEL base.image="mambaorg/micromamba:0.27.0"
LABEL dockerfile.version="1"
LABEL software="GAMBITTOOLS"
LABEL description="Companion tools for working with GAMBIT"
LABEL website="https://github.com/gambit-suite/gambit-tools"
LABEL license="https://github.com/gambit-suite/gambit-tools/blob/master/LICENSE"
LABEL maintainer1="Andrew Page"
LABEL maintainer.email1="andrew.page@theiagen.com"

# Environment
ENV LC_ALL=C.UTF-8

# Install mamba environment
COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1  # Subsequent RUN commands use environment

RUN mamba install -y gambit

# Install gambittools
ADD . /gambittools
WORKDIR /gambittools
RUN pip3 install .

RUN micromamba clean -a -y

USER root
RUN mkdir $GAMBITDB_DB_PATH /data && \
  chown $MAMBA_USER:$MAMBA_USER /data
USER $MAMBA_USER
WORKDIR /data

# Make sure conda, python, and GAMBITtools are in the path
ENV PATH="/opt/conda/bin:${PATH}"

RUN cd /gambittools && bash run_tests.sh

