""" Logger """
import logging.config
from typing import override
import logging
import json
import datetime as dt

################################################################################

def setup_logging(path: str):
    # config_file = pathlib.Path(path)
    with open(path) as f:
        config = json.load(f)
    logging.config.dictConfig(config)

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}

class JSONFormatter(logging.Formatter):
    
    def __init__(self, 
                 *,
                 fmt_keys: dict[str, str] | None = None
                # fmt: str | None = None, datefmt: str | None = None, 
                # style: Literal['%'] | Literal['{'] | Literal['$'] = "%", 
                # validate: bool = True, *, 
                # defaults: logging.Mapping[str, logging.Any] | None = None
            ) -> None:
        super().__init__() #fmt, datefmt, style, validate, defaults=defaults)
        self.fmt_keys = fmt_keys or {}    
    @override
    def format(self, record: logging.LogRecord)-> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)
    
    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat()
        }
        if record.exc_info is not None:
            always_fields['exc_info'] = self.formatException(record.exc_info)
        
        if record.stack_info is not None:
            always_fields['stack_info'] = self.formatStack(record.stack_info)
        
        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val) for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)
        
        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val
        
        return message
        
class NonErrorFilter(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno <= logging.INFO
        
if __name__ == '__main__':
    setup_logging('./logger.json')

    logger = logging.getLogger('root')
    
    logger.debug('DEBUG LOGGER MESSAGE', extra={'extra1':'whateer'})
    logger.error('ERROR LOGGER MESSAGE')
    logger.info('INFOR EERROR')