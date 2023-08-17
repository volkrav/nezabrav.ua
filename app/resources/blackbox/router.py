from fastapi import APIRouter
from app.resources.blackbox.api import get_comment_from_blackbox
from app.resources.blackbox.schemes import SBlackboxComment, SResponseMessageFromBlackbox

router = APIRouter(
    prefix='/blackbox',
    tags=['BlackBox'],
)


@router.get('/{phone}')
async def get_customer_from_blackbox(phone: str):
    return await get_comment_from_blackbox(phone)
