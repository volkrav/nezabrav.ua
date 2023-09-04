from app.dao.base import BaseDAO
from app.reports.models import Reports


class ReportsDAO(BaseDAO):
    model = Reports
