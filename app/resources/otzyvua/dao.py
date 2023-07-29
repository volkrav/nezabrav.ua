from app.dao.base import BaseDAO
from app.resources.otzyvua.models import OtzyvuaComment


class OtzyvuaDAO(BaseDAO):
    model = OtzyvuaComment
