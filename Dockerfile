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
USER root

# Install system dependencies
RUN sudo apt-get update && sudo apt-get install -y libxkbcommon-dev libxkbcommon-tools libxcb-xinerama0 libxcb-xkb1 libxcb-render-util0 libxcb-icccm4 libxcb-keysyms1 libxcb1 libxcb1-dev libxcb-image0
RUN sudo apt-get install qtbase5-dev=5.15.3+dfsg-2ubuntu0.2 qtchooser qt5-qmake qtbase5-dev-tools

# Install mamba environment
COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1  # Subsequent RUN commands use environment

RUN micromamba install -c conda-forge -y zlib sqlite 
RUN micromamba install -c bioconda -c conda-forge -y gambit
RUN pip install PyQt5==5.15.3

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
