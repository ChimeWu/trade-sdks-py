# doc: https://bybit-exchange.github.io/docs/v5/market/orderbook

from pydantic import BaseModel
from typing import Optional, List
from bybit_sdk import BybitReqType


class GetOrderbookQueryParams(BaseModel):
    category: str  # spot, linear, inverse, option
    symbol: str
    limit: Optional[int] = None  # 1-200, 默认 200


class OrderbookItem(BaseModel):
    price: str
    size: str


class GetOrderbookResponseData(BaseModel):
    s: str  # symbol
    b: List[OrderbookItem]  # bids
    a: List[OrderbookItem]  # asks
    ts: Optional[int] = None  # timestamp
    u: Optional[int] = None  # update id


class GetOrderbookReqType(
    BybitReqType[GetOrderbookQueryParams, GetOrderbookResponseData]
):
    METHOD: str = "GET"
    PATH: str = "/v5/market/orderbook"
    SHOULD_SIGN: bool = False

    def __init__(
        self,
        category: str,
        symbol: str,
        limit: Optional[int] = None,
    ):
        param = GetOrderbookQueryParams(
            category=category,
            symbol=symbol,
            limit=limit,
        )
        super().__init__(param)
