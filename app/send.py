import asyncio
from aio_pika import connect, Message


RABBIT_MQ_URL = "amqp://guest:guest@localhost/"


async def send_main(loop):
    connection = await connect(RABBIT_MQ_URL, loop=loop)
    channel = await connection.channel()

    await channel.default_exchange.publish(
        Message(b'{"key": "111", "value": "test value 1"}'),
        routing_key="send_queue",
    )
    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_main(loop))
