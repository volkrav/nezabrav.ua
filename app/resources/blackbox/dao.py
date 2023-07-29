from app.dao.base import BaseDAO
from app.resources.blackbox.models import BlackboxComment


class BlackboxDAO(BaseDAO):
    model = BlackboxComment
