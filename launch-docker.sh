#!/bin/sh

docker run -it --rm -p 8888:8888 \
	-v ${PWD}:/home/jovyan/work eturkes/pymice-notebook:py3.5.4 \
	/bin/bash -c "source activate pymice && jupyter notebook"
