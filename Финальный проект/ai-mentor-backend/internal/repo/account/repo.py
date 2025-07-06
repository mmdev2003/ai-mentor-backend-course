from opentelemetry.trace import SpanKind, Status, StatusCode

from .query import *
from internal import model
from internal import interface


class AccountRepo(interface.IAccountRepo):
    def __init__(self, tel: interface.ITelemetry, db: interface.IDB):
        self.db = db
        self.tracer = tel.tracer()

    async def create_account(self, login: str, password: str) -> int:
        with self.tracer.start_as_current_span(
                "AccountRepo.create_account",
                kind=SpanKind.INTERNAL,
                attributes={
                    "login": login,
                }
        ) as span:
            try:
                args = {
                    'login': login,
                    'password': password,
                }
                account_id = await self.db.insert(create_account, args)

                span.set_status(StatusCode.OK)
                return account_id
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_account_by_login(self, login: str) -> list[model.Account]:
        with self.tracer.start_as_current_span(
                "AccountRepo.get_account_by_login",
                kind=SpanKind.INTERNAL,
                attributes={
                    "login": login,
                }
        ) as span:
            try:
                args = {'login': login}
                rows = await self.db.select(get_account_by_login, args)
                result = model.Account.serialize(rows) if rows else []

                span.set_status(StatusCode.OK)
                return result
            except Exception as err:
                span.record_exception(err)
                span.set_status(StatusCode.ERROR, str(err))
                raise err