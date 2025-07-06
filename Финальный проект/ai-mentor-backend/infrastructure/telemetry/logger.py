import logging

import inspect
from typing import Union

import asyncio
from opentelemetry import trace
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler

from internal import common
from internal import interface

from .alertmanger import AlertManager


class OtelLogger(interface.IOtelLogger):
    def __init__(
            self,
            alert_manger: AlertManager | None,
            logger_provider: LoggerProvider,
            service_name: str,
    ):
        self.handler = LoggingHandler(
            level=logging.DEBUG,
            logger_provider=logger_provider
        )
        self.service_name = service_name
        self.logger = logging.getLogger("main")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)
        self.logger.propagate = False

        self.alert_manger = alert_manger

    def log(self, level: str, message: str, fields: dict = None) -> None:
        file_info = self._get_caller_info(3)
        attributes: dict = {common.FILE_KEY: file_info}

        if fields:
            extra_fields = self._extract_extra_params(fields)
            if extra_fields:
                # attributes[common.EXTRA_LOG_FIELDS_KEY] = extra_fields
                attributes.update(extra_fields)

        current_span = trace.get_current_span()
        if current_span and current_span.get_span_context().is_valid:
            span_context = current_span.get_span_context()

            trace_id = format(span_context.trace_id, '032x')
            span_id = format(span_context.span_id, '016x')

            attributes[common.TRACE_ID_KEY] =trace_id
            attributes[common.SPAN_ID_KEY] =span_id

            if level == "ERROR":
                if self.alert_manger is not None:
                    self.alert_manger.send_error_alert(trace_id, span_id)

        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.log(log_level, self.service_name + " | " + message, extra=attributes)



    def _extract_extra_params(self, fields: dict) -> dict:
        extra_attrs = {}
        for key, value in fields.items():
            if value is None:
                value = ""

            extra_attrs[key] = self._convert_value(value)
        return extra_attrs

    def _convert_value(self, value) -> Union[str, int, float, bool]:
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)

    def _get_caller_info(self, skip: int) -> str:
        try:
            frame = inspect.currentframe()
            for _ in range(skip):
                if frame is None:
                    break
                frame = frame.f_back

            if frame is None:
                return "unknown:0"

            filename = frame.f_code.co_filename
            line_number = frame.f_lineno

            return f"{filename}:{line_number}"
        except Exception:
            return "unknown:0"

    def debug(self, message: str, fields: dict = None) -> None:
        self.log("DEBUG", message, fields)

    def info(self, message: str, fields: dict = None) -> None:
        self.log("INFO", message, fields)

    def warning(self, message: str, fields: dict = None) -> None:
        self.log("WARN", message, fields)

    def error(self, message: str, fields: dict = None) -> None:
        self.log("ERROR", message, fields)
