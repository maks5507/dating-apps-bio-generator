import amqp from "amqplib"
import msgpack from "msgpack"

const TIMEOUT = 60 * 1000

const connection = {
    current: null,
}

const channel = {
    current: null,
}

const pack = payload => msgpack.pack(payload)
const unpack = payload => msgpack.unpack(payload.content)

const connect = async () => { // async connection to the AMQP queue
    if (connection.current === null) {
        console.log(`Opening amqp connection...`)
        connection.current = Promise.resolve(
            amqp.connect(process.env.AMQP_CONNECTION)
        )
    }
    return connection.current
}

const openChannel = async () => {
    if (channel.current === null) {
        console.log(`Opening amqp channel...`)
        channel.current = Promise.resolve(
            connect().then(connection => connection.createChannel())
        )
    }
    return channel.current
}

const consume = (channel, recvQueue) => { // implementation of 'listen' method
    return new Promise(resolve => {
        channel.consume(recvQueue, resolve)
    })
}

const fetch = (exchange, keys, message) => { // implementation of 'fetch' method
    return openChannel().then(async channel => {
        const queue = await channel.assertQueue("", { exclusive: true })

        keys = [].concat(keys)

        channel.publish(exchange, keys[0], pack(message), {
            BCC: keys.slice(1),
            replyTo: queue.queue,
        })

        return new Promise((resolve, reject) => { // temporary queue deleted on timeout
            const fetchTimeout = setTimeout(() => {
                channel.deleteQueue(queue.queue)
                reject(new Error("Timeout error"))
            }, TIMEOUT)

            consume(channel, queue.queue) // waiting for the response message
                .then(message => {
                    if (message === null) throw new Error()
                    clearTimeout(fetchTimeout)
                    channel.ack(message)
                    console.log("Packed response:", message)
                    return message
                })
                .then(unpack) // unpacking the response
                .then(response => {
                    console.log("Unpacked response:", response)
                    if (response.errors && response.errors.length > 0) // checking for errors
                        reject(new Error(response.errors[0]))
                    else resolve(response.data)
                })
                .catch(() => null)
        }).finally(() => {
            channel.deleteQueue(queue.queue)
        })
    })
}

const listen = async (exchange, type, keys, resolve) => { // creates new temporary queue if there is no binding with the specified routing key
    openChannel().then(async channel => {
        channel.assertExchange(exchange, type, { durable: false })

        const queue = await channel.assertQueue("", { exclusive: true })

        keys = [].concat(keys)
        keys.forEach(key => channel.bindQueue(queue.queue, exchange, key))

        channel.consume(queue.queue, async message => {
            const response = await resolve(msgpack.unpack(message.content))

            channel.ack(message)

            if (message.properties.replyTo !== void 0) {
                channel.publish("", message.properties.replyTo, msgpack.pack(response))
            }
        })
    })
}

const shutdown = async () => {
    if (channel.current !== null) {
        console.log(`Closing amqp channel...`)
        await channel.current.then(channel => channel.close())
    }

    if (connection.current !== null) {
        console.log(`Closing amqp connection...`)
        await connection.current.then(connection => connection.close())
    }
}

export default {
    fetch,
    listen,
    shutdown,
}
