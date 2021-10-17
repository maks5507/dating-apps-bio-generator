FROM continuumio/anaconda3 AS build ### change to more lightweight image

ARG core_queue
ARG rmq_connect

RUN apt update; apt install vim procps build-essential git -y;
RUN export OMP_NUM_THREADS=1 #### check if huggingface resolved this issue

COPY . /root/

RUN pip install -r /root/requirements.txt
RUN python /root/setup/init_amqp.py -c $rmq_connect -q $core_queue

RUN cd /root/; python setup.py build; pip install .;

