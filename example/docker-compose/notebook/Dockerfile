FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev curl
RUN pip3 install --upgrade pip
RUN pip install -q jupyter

WORKDIR /notebook

RUN mkdir /notebook/ipynb
COPY ./docker-compose/notebook/setup.sh /notebook/setup.sh
COPY Online_Retail_Analysis.ipynb /notebook/ipynb/Online_Retail_Analysis.ipynb
COPY load_data.py /notebook/load_data.py
COPY requirements-example.txt /notebook/requirements.txt

RUN chmod +x /notebook/setup.sh

ENTRYPOINT [ "/bin/sh" ]