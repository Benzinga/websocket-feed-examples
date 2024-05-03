import aiohttp
import asyncio
import json
import html
import logging
import os
import sys

async def consumer(message):
    try:
        payload = json.loads(message)
        event_info = {
            'kind': payload["kind"],
            'id': payload["data"]["id"],
            'action': payload["data"]["action"],
            'ts': payload["data"]["timestamp"]
        }

        if payload["data"].get("content"):
            event_info.update({
                'content_id': payload["data"]["content"]["id"],
                'title': html.unescape(payload["data"]["content"]["title"])
            })
            event_template = "{kind} event received.\n\tAction: {action}\n\tEvent ID: {id}\n\tContent ID: {content_id}\n\tTitle: {title}\n\tTimestamp(UTC): {ts}\n"
        else:
            event_template = "{kind} event received.\n\tAction: {action}\n\tEvent ID: {id}\n\tTimestamp(UTC): {ts}\n"

        print(event_template.format(**event_info))
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from message")
    except KeyError as e:
        logging.error(f"Missing key in JSON data: {e}")

async def runStream():
    bz_api_key = os.getenv('BZ_API_KEY')
    if not bz_api_key:
        sys.exit('BZ_API_KEY must not be empty')

    uri = f'wss://api.benzinga.com/api/v1/news/stream?token={bz_api_key}'
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Connecting to {uri}")

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(uri, max_msg_size=10_000_000_000) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await consumer(msg.data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

if __name__ == '__main__':
    asyncio.run(runStream())
