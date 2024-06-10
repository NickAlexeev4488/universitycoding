import typing as tp


class RequestParam(tp.TypedDict):
    key: str
    value: str


class Error(tp.TypedDict):
    error_code: int
    error_msg: str
    request_params: tp.List[RequestParam]


class APIError(Exception):
    def __init__(self, response: tp.Dict[str, tp.Any]):
        error: Error = tp.cast(Error, response.get("error"))
        self.error_code = error.get("error_code")
        self.error_msg = error.get("error_msg")
        self.request_params = error.get("request_params")
        super().__init__(self.error_msg)
