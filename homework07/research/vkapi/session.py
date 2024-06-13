import typing as tp

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests_toolbelt.sessions import BaseUrlSession


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, default_timeout: float = 5.0, *args, **kwargs):
        self.timeout = default_timeout
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return super().send(request, **kwargs)


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.retry = Retry(
            status_forcelist=[429, 500, 502, 503, 504],
            # allowed_methods=["HEAD", "GET", "OPTIONS"],
            total=max_retries,
            backoff_factor=backoff_factor
        )
        self.client_session = BaseUrlSession(base_url=self.base_url)
        adapter = TimeoutHTTPAdapter(default_timeout=timeout, max_retries=self.retry)
        self.client_session.mount("https://", adapter)
        self.client_session.mount("http://", adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self.client_session.get(url, *args, **kwargs)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self.client_session.post(url, *args, **kwargs)
