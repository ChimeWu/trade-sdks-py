from bybit_sdk import BybitSDKClient
from bybit_sdk.market.get_instruments_info import (
    GetInstrumentsInfoReqType,
    GetInstrumentsInfoQueryParams,
)

import pytest


@pytest.mark.asyncio
async def test_get_instruments_info():
    api_key = "your_api_key"
    secret = "your_secret_key"
    client = BybitSDKClient(api_key, secret)
    param = GetInstrumentsInfoQueryParams(category="spot")
    req = GetInstrumentsInfoReqType(param)
    resp = await client.send_request(req)
    assert resp.retCode == 0
    assert resp.result is not None
