import json
from pprint import pprint
from typing import List
from fastapi import APIRouter
from app.resources.blackbox.api import get_comment_from_blackbox

from app.resources.blackbox.dao import BlackboxDAO
from app.resources.blackbox.models import BlackboxComment
from app.resources.blackbox.schemes import SBlackboxComment
from app.resources.otzyvua.dao import OtzyvuaDAO

router = APIRouter(
    prefix='/search',
    tags=['Search'],
)


@router.get('/{phone}')
async def get_comments_from_resources(phone: str):# -> List[SBlackboxComment]:
    # comments: List[BlackboxComment] = await BlackboxDAO.find_all_filter_by(phone=phone)
    comment_from_otzyvua = await OtzyvuaDAO.find_all_filter_by(phone=phone)
    comment_from_blackbox = await get_comment_from_blackbox(phone)
    return comment_from_otzyvua + comment_from_blackbox
    # comment: BlackboxComment
    # for comment in comments:
    #     print(comment.id, comment.phone)
    #     for fio in comment.fios:
    #         print(fio)
    #     for track in json.loads(comment.tracks):
    #         pprint(track)
    # return comments
