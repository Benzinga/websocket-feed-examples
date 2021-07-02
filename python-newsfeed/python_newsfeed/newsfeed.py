import asyncio
import html
import logging
import json
import os
import signal
import sys
import websockets

BZ_API_KEY = os.getenv('BZ_API_KEY', default='')


def consumer(message):
    payload = json.loads(message)

    if payload["data"]["content"]:
        print("{kind} event received.\n\tAction: {action}\n\tEvent ID: {id}\n\tContent ID: {content_id}\n\tTitle: {title}\n\tTimestamp(UTC): {ts}\n".format(
            kind=payload["kind"],
            id=payload["data"]["id"],
            action=payload["data"]["action"],
            content_id=payload["data"]["content"]["id"],
            title=html.unescape(payload["data"]["content"]["title"]),
            ts=payload["data"]["timestamp"]
        ))
    else:
        print("{kind} event received.\n\tAction: {action}\n\tEvent ID: {id}\n\tTimestamp(UTC): {ts}\n".format(
            kind=payload["kind"],
            id=payload["data"]["id"],
            action=payload["data"]["action"],
            ts=payload["data"]["timestamp"]
        ))


async def runStream():
    if BZ_API_KEY == '':
        sys.exit('BZ_API_KEY must not be empty')

    uri = 'wss://api.benzinga.com/api/v1/news/stream?token={key}'.format(
        key=BZ_API_KEY)

    logger = logging.getLogger('websockets')
    logger.setLevel(logging.INFO)  # change to debug if needed
    logger.addHandler(logging.StreamHandler())

    logging.info("connecting to {}", uri)

    # messages can be over 1MB, increase max_size from default
    async with websockets.connect(uri, max_size=10_000_000_000) as websocket:
        # Close the connection when receiving SIGTERM.
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(
            signal.SIGTERM, loop.create_task, websocket.close())

        async for message in websocket:
            # This is where you would call your logic.
            consumer(message)

# run until disconnect
asyncio.get_event_loop().run_until_complete(runStream())
