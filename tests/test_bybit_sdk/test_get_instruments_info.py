from bybit_sdk import BybitSDKClient
from bybit_sdk.market.get_instruments_info import (
    GetSpotInstrumentsInfoReqType,
    GetLinearInverseInstrumentsInfoReqType,
    GetOptionInstrumentsInfoReqType,
)

import pytest


@pytest.mark.asyncio
async def test_get_instruments_info():
    api_key = "your_api_key"
    secret = "your_secret_key"
    client = BybitSDKClient(api_key, secret)
    resp = await client.send_request(GetSpotInstrumentsInfoReqType())
    assert resp.retCode == 0
    assert resp.result is not None
    resp = await client.send_request(GetLinearInverseInstrumentsInfoReqType())
    assert resp.retCode == 0
    assert resp.result is not None
    resp = await client.send_request(GetOptionInstrumentsInfoReqType())
    assert resp.retCode == 0
    assert resp.result is not None
