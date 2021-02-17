import os
import asyncio
import json
from functools import partial

from aio_pika import connect, IncomingMessage, Exchange, Message

from db import db

RABBIT_MQ_URL = os.getenv("RABBIT_MQ_URL", default="amqp://guest:guest@localhost/")


class RPCServiceServer:
    async def connect(self, loop):
        connection = await connect(RABBIT_MQ_URL, loop=loop)
        channel = await connection.channel()

        queue_rpc = await channel.declare_queue("rpc_queue")
        queue_send = await channel.declare_queue("send_queue")

        await queue_send.consume(self.on_message_send, no_ack=True)
        await queue_rpc.consume(partial(self.on_message_rpc, channel.default_exchange))

    def on_message_send(self, message: IncomingMessage):
        data = message.body.decode()
        print(f" [.] Recived message: {data}")

        data = json.loads(data)
        db.add_or_update_value(**data)

    async def on_message_rpc(self, exchange: Exchange, message: IncomingMessage):
        with message.process():
            key = message.body.decode()
            print(f" [.] Recived request: {key}")

            response = db.get_value(key).encode()
            print(f" [.] Sending response: {response}")

            await exchange.publish(
                Message(body=response, correlation_id=message.correlation_id),
                routing_key=message.reply_to,
            )


if __name__ == "__main__":
    print(" [x] Starting RPC service...")
    print(" [x] Awaiting RPC requests")

    loop = asyncio.get_event_loop()
    loop.create_task(RPCServiceServer().connect(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
