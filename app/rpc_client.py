import asyncio
import uuid

from aio_pika import connect, IncomingMessage, Message

RABBIT_MQ_URL = "amqp://guest:guest@localhost/"


class RPCServiceClient:
    def __init__(self, loop):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = loop

    async def connect(self):
        self.connection = await connect(RABBIT_MQ_URL, loop=loop)
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response)

        return self

    def on_response(self, message: IncomingMessage):
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def call(self, key: str):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                key.encode(),
                content_type="application/json",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key="rpc_queue",
        )

        return await future


async def main(loop):
    rpc_client = await RPCServiceClient(loop).connect()

    key = "123"
    print(f" [x] Requesting {key=}")
    response = await rpc_client.call(key)
    print(" [.] Got %r" % response)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
