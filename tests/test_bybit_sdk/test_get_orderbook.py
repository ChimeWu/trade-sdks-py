from bybit_sdk import BybitSDKClient
from bybit_sdk.market.get_orderbook import GetOrderbookReqType
import pytest


@pytest.mark.asyncio
async def test_get_orderbook():
    api_key = "your_api_key"
    secret = "your_secret_key"
    client = BybitSDKClient(api_key, secret)
    resp = await client.send_request(
        GetOrderbookReqType(category="spot", symbol="BTCUSDT", limit=5)
    )
    assert resp.retCode == 0
    assert resp.result is not None
