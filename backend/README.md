# Async Backend, Node.JS

**Author**: Maksim Eremeev (mae9785@nyu.edu)

### Starting an instance

```bash
docker-compose build
docker-compose up -d
```

## Structure

`/amqp` contains the scipt for amqp connection and message forwarding

`index.js` runs the app, controls CORS headers, and features REST API-based interface of communication

## Pipeline

Message from frontend -> (REST API) -> backend accepts the message -> (msgpack) -> backend packs the message into the binary format -> (amqp.js) -> backend sends the message to the AMQP queue -> backend **waits** for the response

In order to avoid explicit blocking of the backend process, we utilize **async** opportunities of Node.JS, thus allowing the backend to process several requests simultaneously, while possibly waiting for responses.

## Env file

The amqp connection parameters are passed through the `env.env` enviroment file.

