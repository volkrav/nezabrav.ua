import asyncio
import json
from datetime import datetime
from pprint import pprint
from typing import Dict, List

import aiofiles
import aiohttp

from app.config import settings
from app.resources.blackbox.dao import BlackboxDAO


async def get_comment_from_blackbox(phone: str):
    session: aiohttp.ClientSession
    async with aiohttp.ClientSession() as session:
        request = {
            'id': 1001,
            'params': {
                'phonenumber': phone,
                'api_key': settings.BLACKBOX_API
            }
        }
        data = json.dumps(request)
        async with session.get(url=f'{settings.BLACKBOX_URL}{data}') as response:
            out = []
            if response.status == 200:
                data = await response.json(content_type='text/html', encoding='utf-8')
        #         with open('app/resources/files/0960968496.json', 'w', encoding='utf-8') as file:
        #             file.write(json.dumps(data, indent=4, ensure_ascii=False))
        # async with aiofiles.open('app/resources/files/0960968496.json', 'r', encoding='utf-8') as file:
        #     data = json.loads(await file.read())
        #     # pprint(data)
                async for comment in parse_comment(data):
                    if comment:
                        current_comment = await BlackboxDAO.find_by_id(comment['id'])
                        if current_comment:
                            out.append(current_comment)
                        else:
                            added = await BlackboxDAO.add(**comment)
                            out.append(comment)
            return out


async def parse_comment(content: Dict) -> Dict:
    if content.get('success') and not content.get('message'):
        for id, data in content['data'].items():
            yield {
                'id': id,
                'fios': data['fios'],
                'phone': data['phone'],
                'phone_formatted': data['phone_formatted'],
                'tracks': json.dumps(data['tracks'], indent=4, ensure_ascii=False),
                # 'city': tracks['city'],
                # 'comment': tracks['comment'],
                # 'cost': tracks['cost'],
                # 'date': tracks['date'],
                # 'type': tracks['type'],
                # 'warehouse': tracks['warehouse'],
            }
    else:
        print('blackbox api getting data error')
        yield


if __name__ == '__main__':
    asyncio.run(get_data())
