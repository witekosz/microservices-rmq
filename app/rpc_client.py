import asyncio
import logging
import uuid

from aio_pika import connect, IncomingMessage, Message

from app import settings


logger = logging.getLogger("rpc_client")


class RPCServiceClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = asyncio.get_event_loop()

    async def connect(self):
        self.connection = await connect(settings.RABBIT_MQ_URL)
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

    async def send_duplex_message(self, key: str):
        logger.info(f" [x] Requesting {key}")
        response = await self.call(key)

        logger.info(f" [.] Response {response}")
        return response

    async def send_simplex_message(self, key, value):
        logger.info(f" [x] Sending {key}, {value}")

        await self.channel.default_exchange.publish(
            Message(
                f'{{"key": "{key}", "value": "{value}"}}'.encode(),
                content_type="application/json",
            ),
            routing_key="send_queue",
        )
