FROM continuumio/miniconda3 


##### Create Conda Env 

RUN conda install conda-lock

COPY conda-lock.yml .

RUN conda-lock install --name primera_env conda-lock.yml

ENV PATH="/opt/conda/envs/primera_env/bin:$PATH"


#### Add python scripts

COPY ./src/ ./src/
RUN pip3 install --upgrade pip setuptools && pip3 install /src
