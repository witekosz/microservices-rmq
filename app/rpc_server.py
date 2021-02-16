import asyncio
import json
from functools import partial

from aio_pika import connect, IncomingMessage, Exchange, Message

import db

RABBIT_MQ_URL = "amqp://guest:guest@localhost/"


async def on_message(exchange: Exchange, message: IncomingMessage):
    with message.process():
        key = message.body.decode()

        response = db.db_get_value(key).encode()

        await exchange.publish(
            Message(
                body=response,
                correlation_id=message.correlation_id
            ),
            routing_key=message.reply_to,
        )


def on_message_send(message: IncomingMessage):
    data = message.body.decode()
    data = json.loads(data)
    db.db_add_or_update_value(**data)    


async def main(loop):
    connection = await connect(RABBIT_MQ_URL, loop=loop)
    channel = await connection.channel()

    queue = await channel.declare_queue("rpc_queue")
    queue_send = await channel.declare_queue("send_queue")

    await queue_send.consume(on_message_send, no_ack=True)
    await queue.consume(partial(
        on_message, channel.default_exchange)
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.create_task(main(loop))
    loop.run_forever()
