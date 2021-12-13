FROM continuumio/anaconda3 AS build

ARG core_queue
ARG rmq_connect

RUN apt update; apt install vim procps build-essential git -y;
# RUN export OMP_NUM_THREADS=1

COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt

COPY . /root/

RUN cd /root/; python setup.py build; pip install .;
RUN python /root/setup/init_amqp.py -c $rmq_connect -q $core_queue

