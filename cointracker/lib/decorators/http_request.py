import inspect
import logging
from http import HTTPStatus
from typing import Callable, Dict

from requests import Session, exceptions
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

logger = logging.getLogger(__name__)

RETRYABLE_STATUS_CODES = [
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
]
DEFAULT_HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
}


def get_retryable_session() -> Session:
    session = Session()
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=2, backoff_factor=1, status_forcelist=RETRYABLE_STATUS_CODES
            )
        ),
    )
    return session


class HTTPRequest(object):
    def __call__(self, f: Callable):
        def wrapper(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
                response.raise_for_status()

                return response.json()
            except exceptions.HTTPError as e:
                func_args = inspect.signature(f).bind(*args, **kwargs).arguments
                func_args_str = ", ".join(
                    map("{0[0]} = {0[1]!r}".format, func_args.items())
                )
                logger.error(
                    f"Encountered HTTP error executing {f.__module__}.{f.__qualname__} ({func_args_str}):\n{e}"
                )
                try:
                    error_details = response.json()
                    logger.error(f"Server error details: {error_details}")
                except ValueError:
                    pass

        return wrapper
