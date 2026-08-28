FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG DEBIAN_FRONTEND=noninteractive
ARG MINICONDA_VERSION=py310_24.11.1-0
ARG MINICONDA_SHA256=7a3cdbb78a642b2b6dd0687c9e09824e53330368ab57406e27d88e25c4fe4e40
ARG RESEARCH_UID=1000
ARG RESEARCH_GID=1000

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    CONDA_ENV_NAME=e2e_carla \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MPLBACKEND=Agg \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        ffmpeg \
        git \
        libgl1 \
        libglib2.0-0 \
        libjpeg-dev \
        libpng-dev \
        libpng16-16 \
        libsm6 \
        libtiff5 \
        libxext6 \
        libxrender1 \
        locales \
        unzip \
        wget \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
        "https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" \
        -o /tmp/miniconda.sh \
    && echo "${MINICONDA_SHA256}  /tmp/miniconda.sh" | sha256sum -c - \
    && bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh \
    && /opt/conda/bin/conda create --yes --name "${CONDA_ENV_NAME}" \
        --override-channels --channel conda-forge \
        python=3.10.15 pip \
    && /opt/conda/bin/conda clean -afy

ENV PATH=/opt/conda/envs/e2e_carla/bin:/opt/conda/bin:${PATH}

COPY docker/requirements-carla-garage.txt /tmp/requirements-carla-garage.txt
COPY docker/requirements-project.txt /tmp/requirements-project.txt

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r /tmp/requirements-carla-garage.txt \
    && python -m pip install --no-cache-dir -r /tmp/requirements-project.txt

RUN groupadd --gid "${RESEARCH_GID}" research \
    && useradd --uid "${RESEARCH_UID}" --gid "${RESEARCH_GID}" \
        --create-home --shell /bin/bash research

WORKDIR /workspace/e2e_Carla_paper
COPY . /workspace/e2e_Carla_paper

RUN python -m pip install --no-cache-dir --no-deps -e /workspace/e2e_Carla_paper \
    && chmod +x /workspace/e2e_Carla_paper/docker/entrypoint.sh \
    && chown -R research:research /workspace/e2e_Carla_paper

USER research

ENTRYPOINT ["/workspace/e2e_Carla_paper/docker/entrypoint.sh"]
CMD ["bash"]

