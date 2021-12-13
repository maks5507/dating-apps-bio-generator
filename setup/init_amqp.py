#
# Created by Maksim Eremeev (eremeev@nyu.edu)
#

import argparse

from amqp_interface import AMQPInterface


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--queue', nargs='*', help='queue name for core worker')
    parser.add_argument('-c', '--connect', nargs='*', help='amqp connection credentials')
    args = parser.parse_args()

    interface = AMQPInterface(url_parameters=args.connect[0])

    interface.create_queue(name=args.queue[0],
                           exchange_to_bind='amq.topic',
                           binding_routing_key=args.queue[0])

