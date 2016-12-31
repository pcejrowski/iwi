#!/bin/bash

docker kill jupyter-wiki
docker rm jupyter-wiki
docker pull pcej/jupyter-wikidata
docker run -p 8888:8888 -it -v ${PWD}/notebooks:/notebooks/nbs --rm --name jupyter-wiki pcej/jupyter-wikidata


