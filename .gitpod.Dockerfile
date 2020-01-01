FROM gitpod/workspace-full

USER root

RUN python3 -m pip install --upgrade \
        pip \
        setuptools \
        wheel \
        twine \
        mypy \
        flake8
