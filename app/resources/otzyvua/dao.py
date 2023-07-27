from app.dao.base import BaseDAO
from app.resources.otzyvua.models import OtzyvuaComments


class OtzyvuaDAO(BaseDAO):
    model = OtzyvuaComments
