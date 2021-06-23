FROM continuumio/miniconda3
ARG ENV_NAME="dai_group_demo"
COPY ./app /app

COPY environment.yml /
RUN conda install -c conda-forge mamba
RUN mamba env create --quiet --name ${ENV_NAME} --file /environment.yml && conda clean -a
ENV PATH /opt/conda/envs/${ENV_NAME}/bin:$PATH

RUN mamba env export --name ${ENV_NAME} > ${ENV_NAME}_exported.yml

WORKDIR "/app"
ENTRYPOINT ["python3"]
CMD [ "dashboard.py"]
