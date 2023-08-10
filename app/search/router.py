from typing import Dict, List, Optional, Union
from fastapi import APIRouter
from app.resources.blackbox.api import get_comment_from_blackbox

from app.resources.blackbox.models import BlackboxComment
from app.resources.blackbox.schemes import SBlackboxComment
from app.resources.otzyvua.dao import OtzyvuaDAO
from app.resources.otzyvua.models import OtzyvuaComment
from app.resources.otzyvua.schemes import SOtzyvuaComment

router = APIRouter(
    prefix='/search',
    tags=['Search'],
)


@router.get('/{phone}')
async def get_comments_from_resources(phone: str) -> List[Union[SOtzyvuaComment, SBlackboxComment]]:
    comments_from_otzyvua: List[OtzyvuaComment] = await OtzyvuaDAO.find_all_filter_by(phone=phone) or []
    comments_from_blackbox: List[BlackboxComment] = await get_comment_from_blackbox(phone) or []
    return comments_from_otzyvua + comments_from_blackbox
