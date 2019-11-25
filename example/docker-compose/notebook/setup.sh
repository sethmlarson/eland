#!/bin/bash

cd /notebook

# Install requirments
#pip install -f requirments.txt

# Wait for Elasticsearch to start up before continuing
ELASTICSEARCH="http://elasticsearch:9200"
until $(curl --output /dev/null --silent $ELASTICSEARCH/_cat/health)
do
  echo waiting for $ELASTICSEARCH to be ready to serve ..
  sleep 3
done


# load data to elasticsearch
# python load_data.py

# Start Jupyter Notebook
jupyter notebook --NotebookApp.token='eland' --ip=0.0.0.0 --no-browser --allow-root --notebook-dir=/notebook/ipynb
