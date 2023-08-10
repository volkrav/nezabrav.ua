import asyncio
import json
from datetime import datetime
from pprint import pprint
from typing import Dict, List

import aiofiles
import aiohttp
from pydantic import Json

from app.config import settings
from app.resources.blackbox.dao import BlackboxDAO
from app.resources.blackbox.schemes import SResponseMessageFromBlackbox


async def processing_message_from_blackbox():
    pass

async def get_comment_from_blackbox(phone: str):
    timeout = aiohttp.ClientTimeout(total=15)
    session: aiohttp.ClientSession
    # async with aiohttp.ClientSession() as session:
    #     request_data = await make_request_data(phone)
    #     try:
    #         async with session.get(url=f'{settings.BLACKBOX_URL}{request_data}', timeout=timeout) as response:
    #             if response.status == 200:
    #                 response_data = await response.json(content_type='text/html', encoding='utf-8')
    #                 print(response_data)
    #     except TimeoutError as err:
    #         print(f'TimeoutError: {err}')
    #     except Exception as err:
    #         print(f'Exception: {err}')
    customer = 'app/resources/files/0960968496.json'
    client_not_found = 'app/resources/files/client_not_found.json'
    error = 'app/resources/files/error.json'
    with open(customer, 'r') as file:
        response_data = json.loads(file.read())

    if response_data:
        comment = await parse_comment(response_data)
    return comment or None



async def parse_comment(content: Dict) -> SResponseMessageFromBlackbox:
    client_found = content.get('message') == None
    response_data = None
    if content.get('success') and client_found:
        response_message = 'success'
        for id, data in content['data'].items():
            data = {
                'id': id,
                'fios': data['fios'],
                'phone': data['phone'],
                'phone_formatted': data['phone_formatted'],
                'tracks': json.dumps(data['tracks'], indent=4, ensure_ascii=False),
            }
        response_data = data

    elif not client_found:
        response_message = 'client not found'
    else:
        response_message = 'blackbox api getting data error'
    return {
        'status': response_message,
        'data': response_data
    }

async def make_request_data(phone: str) -> Json:
    request = {
        'id': 1001,
        'params': {
            'phonenumber': phone,
            'api_key': settings.BLACKBOX_API+'z'
        }
    }
    return json.dumps(request)


if __name__ == '__main__':
    asyncio.run(get_comment_from_blackbox())
