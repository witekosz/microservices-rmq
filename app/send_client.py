import asyncio
import logging

from aio_pika import connect, Message

import settings


logger = logging.getLogger(__name__)


async def send_simplex_message(key, value):
    connection = await connect(settings.RABBIT_MQ_URL)

    async with connection.channel() as channel:
        logger.info(f" [x] Sending {key}, {value}")

        await channel.default_exchange.publish(
            Message(
                f'{{"key": "{key}", "value": "{value}"}}'.encode(),
                content_type="application/json",
            ),
            routing_key="send_queue",
        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_simplex_message(key="321", value="test"))
