from pydantic import BaseModel
from typing import Generic, TypeVar
from httpx import AsyncClient, Response
from urllib.parse import urlencode
import time

BASE_ENDPOINT = "https://api.bybit.com"
BASE_ENDPOINT_TESTNET = "https://api-testnet.bybit.com"

REQ = TypeVar("REQ", bound=BaseModel)
RESP = TypeVar("RESP", bound=BaseModel)


class BybitRespType(BaseModel, Generic[RESP]):
    retCode: int
    retMsg: str
    result: RESP
    retExtInfo: dict
    time: int


class BybitReqType(Generic[REQ, RESP]):
    METHOD: str
    PATH: str
    SHOULD_SIGN: bool

    def __init__(self, param: REQ):
        self.param = param

    async def send(
        self,
        client: AsyncClient,
        api_key: str,
        secret_key: str,
        recv_window: int = 10000,
        test=False,
    ) -> BybitRespType[RESP]:
        url = f"{BASE_ENDPOINT_TESTNET if test else BASE_ENDPOINT}{self.PATH}"
        headers = {}
        params = None
        content = None
        timestamp = int(time.time() * 1000)
        if self.METHOD == "POST":
            para_str = self.param.model_dump_json(exclude_none=True)
            content = para_str
        else:
            query_dict = self.param.model_dump(exclude_none=True)
            query_string = urlencode(query_dict)
            params = query_string
            para_str = f"{url}?{query_string}"
        if self.SHOULD_SIGN:
            sign = BybitReqType.gen_sign(
                api_key, secret_key, timestamp, para_str, recv_window
            )
            headers = {
                "X-BAPI-SIGN": sign,
                "X-BAPI-API-KEY": api_key,
                "X-BAPI-TIMESTAMP": str(timestamp),
                "X-BAPI-RECV-WINDOW": str(recv_window),
                "Content-Type": "application/json",
            }
        headers["Content-Type"] = "application/json"
        response: Response = await client.request(
            self.METHOD, url, headers=headers, params=params, content=content
        )
        response.raise_for_status()
        text = response.text
        print(text)
        return BybitRespType[RESP].model_validate_json(response.text)

    @staticmethod
    def gen_sign(
        api_key: str,
        secret_key: str,
        timestamp: int,
        para_str: str,
        recv_window: int = 10000,
    ) -> str:
        import hmac
        import hashlib

        sign_str = f"{timestamp}{api_key}{recv_window}{para_str}"
        signature = hmac.new(
            secret_key.encode("utf-8"), sign_str.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return signature


class BybitSDKClient:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.client = AsyncClient()

    async def send_request(
        self, req: BybitReqType[REQ, RESP], test=False
    ) -> BybitRespType[RESP]:
        return await req.send(self.client, self.api_key, self.secret_key, test)
