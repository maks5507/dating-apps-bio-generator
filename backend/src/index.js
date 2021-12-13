import express from "express"
import cors from "cors"

import amqp from "./amqp/index.js"

const app = express()
app.use(cors({origin: '*'}))

const port = 22111

app.use(express.json())  // To receive json bodies

app.post('/main', (req, res) => {
    // Check empty request
    if(!req.body) {
        return res.sendStatus(400)
    }

    console.log("Got request body:", req.body)

    const payload = req.body
    const body = {
        "action": "summarize",
        "payload": payload
    }
    const exchange = "amq.topic"
    const routing_key = "main"

    console.log("Task was created:", body)

    amqp.fetch(exchange, routing_key, body)
        .then(task_result => {
            console.log("Result is:", task_result)
            res.send(JSON.stringify(task_result))
        })
        .catch(error => {
            console.log("Error occurred:", error)
            res.status(500).send("")
        })
})

app.listen(port, () => {
    console.log(`Server started on port ${port}`)
})

const shutdown = async signal => {
    console.log(`Got signal ${signal}`)
    console.log(`Shutting down...`)

    await amqp.shutdown()

    process.exit(0)
}

process.on("SIGINT", shutdown)
process.on("SIGTERM", shutdown)
process.on("SIGUSR2", shutdown)
