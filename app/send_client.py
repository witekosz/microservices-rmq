import asyncio
from aio_pika import connect, Message


RABBIT_MQ_URL = "amqp://guest:guest@localhost/"


async def send_simplex_message(loop, key, value):
    connection = await connect(RABBIT_MQ_URL, loop=loop)
    channel = await connection.channel()
    print(f" [x] Sending {key}, {value}")

    await channel.default_exchange.publish(
        Message(
            '{"key": "{key}", "value": "{value}"}'.encode(),
            content_type="application/json",
        ),
        routing_key="send_queue",
    )
    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_simplex_message(loop))
