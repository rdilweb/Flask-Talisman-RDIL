FROM gitpod/workspace-full

USER root

RUN \
    python3 -m pip install \
        pip \
        setuptools \
        wheel \
        twine
