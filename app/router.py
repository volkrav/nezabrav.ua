from fastapi import APIRouter

from app.reports.dao import ReportsDAO
from app.reports.models import ESource, EStatusBlackbox
from app.resources.blackbox.api import (get_reports_from_blackbox,
                                        store_reports_from_blackbox_to_db)
from app.resources.novaposhta.api import get_tracking_from_novaposhta, make_report_from_tracking
from app.resources.novaposhta.schemas import SAddReport


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

@router.get('/nezabrav/{phone}')
async def get_customer_from_nezabrav(phone: str):
    return {
        'reports': await ReportsDAO.find_all_filter_by(phone=phone, source=ESource.nezabrav),
        'status_blackbox': EStatusBlackbox.offline,
    }


@router.post('/add')
async def add_report(form_data: SAddReport):
    try:
        tracking_dict = await get_tracking_from_novaposhta(form_data.ttn, form_data.phone)
        report_dict = await make_report_from_tracking(tracking_dict, form_data)
        await ReportsDAO.add(**report_dict)
        return {
            'success': True,
            'message': (f"Покупець {report_dict['name']}, "
                        f"номер телефону {report_dict['phone']}, "
                        f"внесений до реєстру згідно ЕН {report_dict['TTN']}"),
        }
    except Exception as err:
        return {
            'success': False,
            'message': err.args[0] if err.args else "Unspecified error",
        }
