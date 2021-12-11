import amqp from "amqplib"
import msgpack from "msgpack"
// import { TimeoutError } from "./errors/index.js"  // TODO: Fix it

const TIMEOUT = 60 * 1000

const connection = {
    current: null,
}

const channel = {
    current: null,
}

const pack = payload => msgpack.pack(payload)
const unpack = payload => msgpack.unpack(payload.content)

const connect = async () => {
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

const consume = (channel, recvQueue) => {
    return new Promise(resolve => {
        channel.consume(recvQueue, resolve)
    })
}

const fetch = (exchange, keys, message) => {
    return openChannel().then(async channel => {
        const queue = await channel.assertQueue("", { exclusive: true })

        keys = [].concat(keys)

        channel.publish(exchange, keys[0], pack(message), {
            BCC: keys.slice(1),
            replyTo: queue.queue,
        })

        return new Promise((resolve, reject) => {
            const fetchTimeout = setTimeout(() => {
                channel.deleteQueue(queue.queue)
                reject(new Error("Timeout error"))  // TODO: TimeoutError({ exchange, keys, ...message }))
            }, TIMEOUT)

            consume(channel, queue.queue)
                .then(message => {
                    if (message === null) throw new Error()
                    clearTimeout(fetchTimeout)
                    channel.ack(message)
                    console.log("Packed response:", message)
                    return message
                })
                .then(unpack)
                .then(response => {
                    console.log("Unpacked response:", response)
                    if (response.errors && response.errors.length > 0)
                        reject(new Error(response.errors[0]))
                    else resolve(response.data)
                })
                .catch(() => null)
        }).finally(() => {
            channel.deleteQueue(queue.queue)
        })
    })
}

const listen = async (exchange, type, keys, resolve) => {
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
