#
# Created by Maksim Eremeev (mae9785@nyu.edu)
#

import amqp_interface
import msgpack


class Worker:

    def __init__(self, action, log):
        self.log = log
        self.action = action

    @amqp_interface.class_consumer
    def __read(self, payload, props):
        """
        :param payload: payload from message, should be msgpacked
        :param props: message properties, ignored
        """
        try:
            data = msgpack.unpackb(payload, raw=False)

            action_type = data['action']
            params = data['payload']
            params['action'] = action_type

            result = self.action(**params)

            result = msgpack.packb(result)
        except:
            self.log.failure('')
            result = msgpack.packb({'data': [], 'errors': ['launcher error']})
        return result

    def run(self, rmq_connect, rmq_queue):
        """
        :param rmq_connect: url-based parameters to connect to the messsage queue. Sample: amqp://guest:guest@localhost:5672
        :param rmq_queue: queue name to connect
        """
        try:
            interface = amqp_interface.AMQPInterface(url_parameters=rmq_connect)
            interface.listen(rmq_queue, self.__read)
        except Exception:
            self.log.failure('')
