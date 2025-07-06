from typing import Any, Sequence

from opentelemetry.trace import Status, StatusCode, SpanKind
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from internal import interface


def NewPool(
        db_user,
        db_pass,
        db_host
        , db_port,
        db_name
):
    async_engine = create_async_engine(
        f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}",
        echo=False,
        future=True,
        pool_size=15,
        max_overflow=15,
        pool_recycle=300
    )

    pool = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False
    )
    return pool


class PG(interface.IDB):

    def __init__(self, tel: interface.ITelemetry, db_user, db_pass, db_host, db_port, db_name):
        self.pool = NewPool(db_user, db_pass, db_host, db_port, db_name)
        self.tracer = tel.tracer()

    async def insert(self, query: str, query_params: dict) -> int:
        with self.tracer.start_as_current_span(
                "PG.insert",
                kind=SpanKind.CLIENT,
        ) as span:
            try:
                async with self.pool() as session:
                    result = await session.execute(text(query), query_params)
                    rows = result.all()
                    await session.commit()
                    span.set_status(Status(StatusCode.OK))
                    return rows[0][0]

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def delete(self, query: str, query_params: dict) -> None:
        with self.tracer.start_as_current_span(
                "PG.delete",
                kind=SpanKind.CLIENT,
        ) as span:
            try:
                async with self.pool() as session:
                    await session.execute(text(query), query_params)
                    await session.commit()
                    span.set_status(Status(StatusCode.OK))
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def update(self, query: str, query_params: dict) -> None:
        with self.tracer.start_as_current_span(
                "PG.update",
                kind=SpanKind.CLIENT,
        ) as span:
            try:
                async with self.pool() as session:
                    await session.execute(text(query), query_params)
                    await session.commit()
                    span.set_status(Status(StatusCode.OK))
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def select(self, query: str, query_params: dict) -> Sequence[Any]:
        with self.tracer.start_as_current_span(
                "PG.select",
                kind=SpanKind.CLIENT,
        ) as span:
            try:
                async with self.pool() as session:
                    result = await session.execute(text(query), query_params)
                    await session.commit()
                    rows = result.all()
                    span.set_status(Status(StatusCode.OK))
                    return rows
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def multi_query(
            self,
            queries: list[str]
    ) -> None:
        async with self.pool() as session:
            for query in queries:
                await session.execute(text(query))
            await session.commit()
        return None
