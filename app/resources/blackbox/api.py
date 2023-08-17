import asyncio
import json
from datetime import datetime
from pprint import pprint
from typing import Dict, List

import aiofiles
import aiohttp
from pydantic import Json

from app.config import settings
from app.exceptions import (BlackboxRequestTimeoutExpired,
                            ClientNotFoundInBlackbox, GetErrorFromApiBlackbox)
from app.reports.dao import ReportsDAO
from app.reports.models import ESource

# from app.resources.blackbox.dao import BlackboxDAO
# from app.resources.blackbox.schemes import SResponseMessageFromBlackbox


async def processing_reports_from_blackbox(reports: List):
    for report in reports:
        if not await ReportsDAO.find_one_or_none(ext_id=report['ext_id']):
            await ReportsDAO.add(**report)


async def get_comment_from_blackbox(phone: str):
    timeout = aiohttp.ClientTimeout(total=20)
    session: aiohttp.ClientSession
    async with aiohttp.ClientSession() as session:
        request_data = await make_request_data(phone)
        try:
            async with session.get(url=f'{settings.BLACKBOX_URL}{request_data}', timeout=timeout) as response:
                if response.status == 200:
                    response_data = await response.json(content_type='text/html', encoding='utf-8')
        except TimeoutError:
            raise BlackboxRequestTimeoutExpired
        except Exception as err:
            print(f'Exception: {err}')
    # customer = 'app/resources/files/0960968496.json'
    # client_not_found = 'app/resources/files/client_not_found.json'
    # error = 'app/resources/files/error.json'
    # with open(client_not_found, 'r') as file:
    #     response_data = json.loads(file.read())

    if response_data:
        reports = await parse_comment(response_data)
        await processing_reports_from_blackbox(reports)
        return reports


async def parse_comment(content: Dict):
    client_found = content.get('message') == None
    if not client_found:
        raise ClientNotFoundInBlackbox
    get_error = content.get('error')
    if get_error:
        GetErrorFromApiBlackbox.detail = f"{get_error['message']} (code {get_error['code']})"
        raise GetErrorFromApiBlackbox
    if content.get('success') and client_found:
        reports = []
        for _, data in content['data'].items():
            tracks = data.get('tracks', [])
            for track in tracks:
                reports.append({
                    'ext_id': str(track['id']),
                    'source': ESource.blackbox,
                    'created': datetime.utcnow(),
                    'updated': datetime.utcnow(),
                    'phone': data['phone'],
                    'name': data['fios'][0],
                    'extra_names': data['fios'][1:] or None,
                    'report': track['comment'],
                    'carrier': track['type'],
                    'city': track['city'],
                    'warehouse': track['warehouse'],
                    'losses': int(track['cost']),
                    'shipment_date': datetime.strptime(track['date'], '%d.%m.%Y %H:%M:%S') if track['date'] else None,
                })
        return reports


async def make_request_data(phone: str) -> Json:
    request = {
        'id': 1001,
        'params': {
            'phonenumber': phone,
            'api_key': settings.BLACKBOX_API
        }
    }
    return json.dumps(request)


if __name__ == '__main__':
    asyncio.run(get_comment_from_blackbox('0960968496'))
