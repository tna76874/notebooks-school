FROM jupyter/scipy-notebook:python-3.8.13

USER root

ENV SETUP_STATUS="production"
ENV REPO_USER="tna76874"
ENV REPO_NAME="notebooks-school"

COPY ./scripts/docker-entrypoint.sh /
COPY ./scripts/update_notebooks /usr/local/bin/
RUN chmod 775 /usr/local/bin/update_notebooks

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -q && apt-get install -y \
    ghostscript \
    python3-tk &&\
    rm -rf /var/lib/apt/lists/*

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN chmod 775 /docker-entrypoint.sh


USER ${NB_USER}

COPY ./requirements.txt . 

RUN python3 -m pip install --no-cache-dir notebook jupyterlab jupyterhub &&\
    pip install --no-cache-dir -r requirements.txt &&\
    pip install jupyter_contrib_nbextensions ipywidgets &&\
    jupyter contrib nbextension install --user &&\
    jupyter nbextension enable varInspector/main && \
    rm -rf requirements.txt

RUN rm -rf ${HOME}/work

ENTRYPOINT ["/docker-entrypoint.sh"]