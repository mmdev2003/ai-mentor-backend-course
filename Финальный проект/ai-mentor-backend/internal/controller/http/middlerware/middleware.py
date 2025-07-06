import time
from typing import Callable
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from opentelemetry import propagate
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import SpanKind, Status, StatusCode

from internal import interface
from internal import common


class HttpMiddleware(interface.IHttpMiddleware):
    def __init__(
            self,
            tel: interface.ITelemetry,
            prefix: str,
    ):
        self.tracer = tel.tracer()
        self.meter = tel.meter()
        self.logger = tel.logger()
        self.prefix = prefix

    def trace_middleware01(self, app: FastAPI):
        @app.middleware("http")
        async def _trace_middleware01(request: Request, call_next: Callable):
            if self.prefix not in request.url.path:
                return JSONResponse(
                    status_code=404,
                    content={"error": "not found"}
                )
            with self.tracer.start_as_current_span(
                    f"{request.method} {request.url.path}",
                    context=propagate.extract(dict(request.headers)),
                    kind=SpanKind.SERVER,
                    attributes={
                        SpanAttributes.HTTP_ROUTE: str(request.url.path),
                        SpanAttributes.HTTP_METHOD: request.method,
                    }
            ) as root_span:
                span_ctx = root_span.get_span_context()
                trace_id = format(span_ctx.trace_id, '032x')
                span_id = format(span_ctx.span_id, '016x')

                request.state.trace_id = trace_id
                request.state.span_id = span_id
                try:
                    response = await call_next(request)

                    status_code = response.status_code
                    response_size = response.headers.get("content-length")

                    root_span.set_attributes({
                        SpanAttributes.HTTP_STATUS_CODE: status_code,
                    })

                    if response_size:
                        try:
                            root_span.set_attribute(SpanAttributes.HTTP_RESPONSE_BODY_SIZE, int(response_size))
                        except ValueError:
                            pass

                    response.headers[common.TRACE_ID_HEADER] = trace_id
                    response.headers[common.SPAN_ID_HEADER] = span_id

                    if status_code >= 500:
                        err = Exception("Internal server error")
                        root_span.record_exception(err)
                        root_span.set_status(Status(StatusCode.ERROR, str(err)))
                        root_span.set_attribute(common.ERROR_KEY, True)
                        raise err
                    elif status_code >= 400:
                        err = Exception("Client error")
                        root_span.record_exception(err)
                        root_span.set_status(Status(StatusCode.ERROR, str(err)))
                        root_span.set_attribute(common.ERROR_KEY, True)
                        raise err
                    else:
                        root_span.set_status(Status(StatusCode.OK))

                    return response

                except Exception as err:
                    root_span.record_exception(err)
                    root_span.set_status(Status(StatusCode.ERROR, str(err)))
                    root_span.set_attribute(common.ERROR_KEY, True)
                    return JSONResponse(
                        status_code=500,
                        content={"message": "Internal Server Error"},
                    )

        return _trace_middleware01

    def metrics_middleware02(self,app: FastAPI):
        ok_request_counter = self.meter.create_counter(
            name=common.OK_REQUEST_TOTAL_METRIC,
            description="Total count of 200 HTTP requests",
            unit="1"
        )

        error_request_counter = self.meter.create_counter(
            name=common.ERROR_REQUEST_TOTAL_METRIC,
            description="Total count of 500 HTTP requests",
            unit="1"
        )

        request_duration = self.meter.create_histogram(
            name=common.REQUEST_DURATION_METRIC,
            description="HTTP request duration in seconds",
            unit="s"
        )

        request_size = self.meter.create_histogram(
            name=common.REQUEST_BODY_SIZE_METRIC,
            description="HTTP request size in bytes",
            unit="by"
        )

        response_size = self.meter.create_histogram(
            name=common.RESPONSE_BODY_SIZE_METRIC,
            description="HTTP response size in bytes",
            unit="by"
        )

        active_requests = self.meter.create_up_down_counter(
            name=common.ACTIVE_REQUESTS_METRIC,
            description="Number of active HTTP requests",
            unit="1"
        )

        @app.middleware("http")
        async def _metrics_middleware02(request: Request, call_next: Callable):
            start_time = time.time()
            active_requests.add(1)

            trace_id = request.state.trace_id
            span_id = request.state.span_id

            content_length = request.headers.get("content-length")
            request_attrs = {
                SpanAttributes.HTTP_METHOD: request.method,
                SpanAttributes.HTTP_ROUTE: request.url.path,
                common.SPAN_ID_KEY: span_id,
                common.TRACE_ID_KEY: trace_id,
            }
            try:
                if content_length and int(content_length) > 0:
                    request_size.record(int(content_length), attributes=request_attrs)

                response = await call_next(request)

                duration_seconds = time.time() - start_time
                status_code = response.status_code

                request_attrs[common.HTTP_STATUS_KEY] = status_code
                request_attrs[common.HTTP_REQUEST_DURATION_KEY] = duration_seconds

                if status_code >= 500:
                    error_request_counter.add(1, attributes=request_attrs)
                else:
                    ok_request_counter.add(1, attributes=request_attrs)

                request_duration.record(duration_seconds, attributes=request_attrs)
                response_content_length = response.headers.get("content-length")

                if response_content_length:
                    try:
                        response_size.record(int(response_content_length), attributes=request_attrs)
                    except ValueError:
                        pass

                return response
            except Exception as err:
                duration_seconds = time.time() - start_time
                request_attrs[common.HTTP_STATUS_KEY] = 500
                request_attrs[common.ERROR_KEY] = str(err)

                error_request_counter.add(1, attributes=request_attrs)
                request_duration.record(duration_seconds, attributes=request_attrs)
                raise
            finally:
                active_requests.add(-1)

        return _metrics_middleware02

    def logger_middleware03(self, app: FastAPI):
        @app.middleware("http")
        async def _logger_middleware03(request: Request, call_next: Callable):
            start_time = time.time()

            trace_id = request.state.trace_id
            span_id = request.state.span_id

            extra_log = {
                common.HTTP_METHOD_KEY: request.method,
                common.HTTP_ROUTE_KEY: request.url.path,
                common.TRACE_ID_KEY: trace_id,
                common.SPAN_ID_KEY: span_id,
            }
            try:
                self.logger.info("Началась обработка HTTP запроса", extra_log)
                response = await call_next(request)

                status_code = response.status_code

                extra_log = {
                    **extra_log,
                    common.HTTP_REQUEST_DURATION_KEY: time.time() - start_time,
                    common.HTTP_STATUS_KEY: response.status_code,
                }

                if 400 <= status_code < 500:
                    self.logger.warning("Обработка HTTP запроса завершена с ошибкой клиента", extra_log)
                else:
                    self.logger.info("Обработка HTTP запроса завершена успешно", extra_log)

                return response

            except Exception as err:
                extra_log = {
                    **extra_log,
                    common.HTTP_REQUEST_DURATION_KEY: time.time() - start_time,
                    common.HTTP_STATUS_KEY: 500,
                    common.ERROR_KEY: str(err),
                }

                self.logger.error(f"Обработка HTTP запроса завершена с ошибкой", extra_log)
                raise

        return _logger_middleware03
