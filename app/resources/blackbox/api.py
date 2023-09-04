import asyncio
import json
from datetime import datetime
from typing import Dict, List

import aiohttp
from pydantic import Json

from app.config import settings
from app.exceptions import GetErrorFromBlackbox
from app.reports.dao import ReportsDAO
from app.reports.models import ESource, Reports


async def fetch(phone: str):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession() as session:
        request_data = await make_request_data(phone)
        async with session.get(url=f'{settings.BLACKBOX_URL}{request_data}', timeout=timeout) as response:
            if response.status == 200:
                return await response.json(content_type='text/html', encoding='utf-8')


async def store_reports_from_blackbox_to_db(phone: str, reports: List[Reports] | None):
    await ReportsDAO.delete(phone=phone, source=ESource.blackbox)
    if reports:
        for report in reports:
            await ReportsDAO.add(**report)


async def get_reports_from_blackbox(phone: str):
    # print("work get_reports_from_blackbox")
    # customer = 'app/resources/files/0960968496.json'
    # client_not_found = 'app/resources/files/client_not_found.json'
    # error = 'app/resources/files/error.json'
    # with open(customer, 'r') as file:
    #     response_data = json.loads(file.read())

    response_data = await fetch(phone)
    if response_data:
        return await parse_response(response_data)


async def parse_response(content: Dict):
    get_error = content.get('error')
    if get_error:
        raise GetErrorFromBlackbox(get_error)
    client_found = content.get('message') == None
    if not client_found:
        return None
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
    asyncio.run(get_reports_from_blackbox('0960968496'))
