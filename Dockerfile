FROM conda/miniconda3

ENV INPUT_CACHE_SHA256 06396d0b456d671716ca6fd99f5915e8f007a5b2771cc9c04c92fa7f9f7299d1

#RUN conda update -n base -c defaults conda 
#RUN conda create -y -n py37 python=3.7
#RUN echo "source activate py37" > ~/.bashrc 
#ENV PATH /opt/conda/envs/py37/bin:$PATH

#RUN /bin/bash -c "source activate py37" 
#RUN source activate py37

#RUN conda env list

RUN apt-get --quiet update && \
    apt-get --quiet --yes dist-upgrade

RUN apt-get install -yq --no-install-recommends \
ca-certificates \
build-essential \
cmake \
wget \
git \
libxext6 \
libxrender-dev \
xz-utils \
vim

RUN conda install -y -c SBMLTeam python-libsbml
RUN conda install -y -c rdkit rdkit
RUN conda install -y -c openbabel openbabel 

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir pytest
RUN pip install --no-cache-dir cobra 
RUN pip install --no-cache-dir scipy

RUN git clone --single-branch --branch galaxy https://mdulac:towlie1988@brsforge.micalis.fr/mdulac/rpFBA.git /home/src/rpFBA/
#WORKDIR /home/mdulac/Documents/rpFBA/

#TODO: change this to ADD or an online source 
WORKDIR /home/src/rpFBA/
COPY input_cache.tar.xz /home/src/rpFBA/
RUN echo "$INPUT_CACHE_SHA256 input_cache.tar.xz" > input_cache.tar.xz.sha256
RUN cat input_cache.tar.xz.sha256
RUN echo $INPUT_CACHE_SHA256

RUN tar -xf /home/src/rpFBA/input_cache.tar.xz -C /home/src/rpFBA/
RUN tar -xf /home/src/rpFBA/component_contribution/data.tar.xz -C /home/src/rpFBA/component_contribution/

#TODO: perform a checksum on the passed parameters

# generate the cache
RUN python /home/src/rpFBA/rpCache.py
RUN mv /home/src/rpFBA/input_cache/cc_preprocess.npz /home/src/rpFBA/cache/
COPY bigg_iMM904.COBRA-sbml3.xml /home/src/rpFBA/test/test_models/

#TODO: run the tests and make sure that they all pass

WORKDIR /home/src/
#reader
COPY wrapRPreader.py /home/src/
RUN chmod 755 /home/src/wrapRPreader.py
RUN ln -s /home/src/wrapRPreader.py /usr/bin
#thermo
COPY wrapRPthermo.py /home/src/
RUN chmod 755 /home/src/wrapRPthermo.py
RUN ln -s /home/src/wrapRPthermo.py /usr/bin
#merge
COPY wrapRPmerge.py /home/src/
RUN chmod 755 /home/src/wrapRPmerge.py
RUN ln -s /home/src/wrapRPmerge.py /usr/bin


#RUN ln -s /home/src/rpFBA /usr/bin
VOLUME /home/src
#COPY input.tar.gz /rpFBA/
#RUN tar -xzvf /rpFBA/input.tar.gz


#TODO: run the tests to make sure that everything is running smoothly

#ENTRYPOINT /bin/bash


#RUN /bin/bash -c ". activate myenv && \
#    pip install pandas && \ 
#    pip install ../mylocal_package/
