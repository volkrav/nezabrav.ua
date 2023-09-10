import asyncio
from collections.abc import Iterator
from datetime import datetime
from enum import Enum, EnumMeta
import json
import traceback
import sys
import logging
from aiohttp import ClientResponseError, ClientSession

from app.config import settings
from app.exceptions import GetErrorFromNovaposhta
from app.reports.models import ECarriers, ESource, Reports
from app.resources.novaposhta.schemas import EStatus, SAddReport, STracking

logger = logging.getLogger(__name__)


async def get_tracking_from_novaposhta(ttn: str, phone: str) -> dict:
    async with ClientSession() as session:
        raw_tracking = await fetch(ttn, phone, session)
    # with open(f'app/resources/novaposhta/{ttn}.json', 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(raw_tracking, ensure_ascii=False, indent=4))
    if not raw_tracking.get('success'):
        logger.error(
            f"The response is not successful:\n"
            f"\twarnings: {raw_tracking['warnings']}\n"
            f"\terrors: {raw_tracking['errors']}\n"
            f"\tcode error: {raw_tracking['errorCodes']}"
        )
        raise GetErrorFromNovaposhta(
            f"ПОМИЛКА! Експрес-накладну з номером {ttn} не знайдено."
        )
    if raw_tracking['warnings']:
        logger.error(
            f"The telephone number {phone} does not correspond "
            f"to the telephone number of the recipient of the TTN {ttn}\n"
            f"\twarnings: {raw_tracking['warnings']}\n"
            f"\terrors: {raw_tracking['errors']}\n"
            f"\tcode error: {raw_tracking['errorCodes']}"
        )
        raise GetErrorFromNovaposhta(
            f"ПОМИЛКА! Номер телефону {phone} не відповідає "
            f"номеру телефону отримувача по ЕН {ttn}."
        )
    try:
        data = raw_tracking['data'][0]
        if data['StatusCode'] not in EStatus:
            logger.error(
                f"The telephone number {phone} does not correspond "
                f"to the telephone number of the recipient of the TTN {ttn}"
            )
            raise GetErrorFromNovaposhta(
                f"Помилка! ЕН {ttn} зі статусом: {data['Status']}, не може бути додана."
            )
        return {
            'Number': data['Number'],
            'DateCreated': data['DateCreated'],
            'PhoneRecipient': data['PhoneRecipient'] or phone,
            'CityRecipient': data['CityRecipient'],
            'WarehouseRecipient': data['WarehouseRecipient'] or data['RecipientAddress'],
            'DocumentCost': data['DocumentCost'],
            'StoragePrice': data['StoragePrice'],
        }
    except GetErrorFromNovaposhta:
        raise
    except Exception:
        logger.exception(
            f'Received an exception when working with the result from the API Novaposhta')
        raise GetErrorFromNovaposhta('Service is unavailable')


async def fetch(ttn: str, phone: str, session: ClientSession) -> dict:
    try:
        async with session.get(
                settings.NOVAPOSHTA_API_URL,
                json=await _make_request_data(
                    ttn,
                    phone)) as response:
            if response.status == 200:
                return await response.json()
            else:
                await response.raise_for_status()
    except Exception:
        logger.exception(
            f'Got an exception status code not 200')
        # logger.error(traceback.format_exc(limit=1))
        raise GetErrorFromNovaposhta('Service is unavailable')


async def _make_request_data(ttn: str, phone: str) -> dict:
    return {
        # "apiKey": "[ВАШ КЛЮЧ]",
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [
                {
                    "DocumentNumber": ttn,
                    "Phone": phone,
                },
            ]
        }
    }


async def make_report_from_tracking(
        tracking: dict,
        form_data: SAddReport,
) -> dict:
    try:
        losses = int(float(tracking['StoragePrice']) if tracking['StoragePrice']
                     else 0 + float(tracking['DocumentCost']))
        return {
            'ext_id': tracking['Number'],
            'source': ESource.nezabrav,
            'created': datetime.utcnow(),
            'updated': datetime.utcnow(),
            'phone': tracking['PhoneRecipient'],
            'name': form_data.last_name + ' ' + form_data.first_name,
            'report': form_data.report,
            'TTN': tracking['Number'],
            'carrier': 'Nova Poshta',
            'city': tracking['CityRecipient'],
            'warehouse': tracking['WarehouseRecipient'],
            'losses': losses,
            'shipment_date': datetime.strptime(tracking['DateCreated'], '%d-%m-%Y %H:%M:%S'),
            # 'user_id': '',
        }
    except Exception:
        logging.exception("Got errors")

if __name__ == '__main__':
    asyncio.run(get_tracking_from_novaposhta('59001019981517', '380999696104'))
