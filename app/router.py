from fastapi import APIRouter

from app.reports.dao import ReportsDAO
from app.reports.models import ESource, EStatusBlackbox
from app.resources.blackbox.api import (get_reports_from_blackbox,
                                        store_reports_from_blackbox_to_db)


router = APIRouter(
    tags=['Search'],
)


@router.get('/blackbox/{phone}')
async def get_customer_from_blackbox(phone: str):
    try:
        reports = await get_reports_from_blackbox(phone)
        await store_reports_from_blackbox_to_db(phone, reports)
        return {
            'reports': reports,
            'status_blackbox': EStatusBlackbox.online,
        }
    except Exception as err:
        #! log(err)
        print(err)
        return {
            'reports': await ReportsDAO.find_all_filter_by(phone=phone, source=ESource.blackbox),
            'status_blackbox': EStatusBlackbox.offline,
        }


@router.get('/otzyvua/{phone}')
async def get_customer_from_otzyvua(phone: str):
    return {
        'reports': await ReportsDAO.find_all_filter_by(phone=phone, source=ESource.otzyvua),
        'status_blackbox': EStatusBlackbox.offline,
    }
