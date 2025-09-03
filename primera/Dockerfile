FROM continuumio/miniconda3 


##### Create Conda Env 

RUN conda install conda-lock

COPY env-lock-linux64.yml .

RUN conda-lock install --name primera_env env-lock-linux64.yml

ENV PATH="/opt/conda/envs/primera_env/bin:$PATH"


#### Add python scripts

COPY ./src/ ./src/
RUN pip3 install --upgrade pip setuptools && pip3 install /src
