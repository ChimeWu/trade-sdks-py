from pydantic import BaseModel
from typing import Optional, List
from bybit_sdk import BybitReqType


class GetInstrumentsInfoQueryParams(BaseModel):
    category: str
    symbol: Optional[str] = None
    status: Optional[str] = None
    baseCoin: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


# spot
class SpotLotSizeFilter(BaseModel):
    basePrecision: str
    quotePrecision: str
    minOrderQty: str
    maxOrderQty: str
    minOrderAmt: str
    maxOrderAmt: str


class SpotPriceFilter(BaseModel):
    tickSize: str


class SpotRiskParameters(BaseModel):
    priceLimitRatioX: str
    priceLimitRatioY: str


class SpotInstrumentsInfoItem(BaseModel):
    symbol: str
    baseCoin: str
    quoteCoin: str
    innovation: str
    status: str
    marginTrading: str
    stTag: str
    lotSizeFilter: SpotLotSizeFilter
    priceFilter: SpotPriceFilter
    riskParameters: SpotRiskParameters


class GetInstrumentsInfoSpotResponseData(BaseModel):
    category: str
    list: List[SpotInstrumentsInfoItem]
    nextPageCursor: Optional[str] = None


# linear & inverse
class LinearInverseLeverageFilter(BaseModel):
    minLeverage: str
    maxLeverage: str
    leverageStep: str


class LinearInversePriceFilter(BaseModel):
    minPrice: str
    maxPrice: str
    tickSize: str


class LinearInverseLotSizeFilter(BaseModel):
    minNotionalValue: str
    maxOrderQty: str
    maxMktOrderQty: str
    minOrderQty: str
    qtyStep: str
    postOnlyMaxOrderQty: str


class LinearInverseRiskParameters(BaseModel):
    priceLimitRatioX: str
    priceLimitRatioY: str


class PreListingPhaseItem(BaseModel):
    phase: str
    startTime: str
    endTime: str


class PreListingAuctionFeeInfo(BaseModel):
    auctionFeeRate: str
    takerFeeRate: str
    makerFeeRate: str


class PreListingInfo(BaseModel):
    curAuctionPhase: str
    phases: List[PreListingPhaseItem]
    auctionFeeInfo: PreListingAuctionFeeInfo


class LinearInverseInstrumentsInfoItem(BaseModel):
    symbol: str
    contractType: str
    status: str
    baseCoin: str
    quoteCoin: str
    launchTime: str
    deliveryTime: str
    deliveryFeeRate: str
    priceScale: str
    leverageFilter: LinearInverseLeverageFilter
    priceFilter: LinearInversePriceFilter
    lotSizeFilter: LinearInverseLotSizeFilter
    unifiedMarginTrade: bool
    fundingInterval: int
    settleCoin: str
    copyTrading: str
    upperFundingRate: str
    lowerFundingRate: str
    displayName: str
    riskParameters: LinearInverseRiskParameters
    isPreListing: bool
    preListingInfo: Optional[PreListingInfo] = None


class GetInstrumentsInfoLinearInverseResponseData(BaseModel):
    category: str
    list: List[LinearInverseInstrumentsInfoItem]
    nextPageCursor: Optional[str] = None


# option
class OptionPriceFilter(BaseModel):
    minPrice: str
    maxPrice: str
    tickSize: str


class OptionLotSizeFilter(BaseModel):
    maxOrderQty: str
    minOrderQty: str
    qtyStep: str


class OptionInstrumentsInfoItem(BaseModel):
    symbol: str
    optionsType: str
    status: str
    baseCoin: str
    quoteCoin: str
    settleCoin: str
    launchTime: str
    deliveryTime: str
    deliveryFeeRate: str
    priceFilter: OptionPriceFilter
    lotSizeFilter: OptionLotSizeFilter
    displayName: str


class GetInstrumentsInfoOptionResponseData(BaseModel):
    category: str
    list: List[OptionInstrumentsInfoItem]
    nextPageCursor: Optional[str] = None


class GetSpotInstrumentsInfoReqType(
    BybitReqType[GetInstrumentsInfoQueryParams, GetInstrumentsInfoSpotResponseData]
):
    METHOD: str = "GET"
    PATH: str = "/v5/market/instruments-info"
    SHOULD_SIGN: bool = False

    def __init__(
        self,
        symbol: Optional[str] = None,
        status: Optional[str] = None,
        baseCoin: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ):
        param = GetInstrumentsInfoQueryParams(
            category="spot",
            symbol=symbol,
            status=status,
            baseCoin=baseCoin,
            limit=limit,
            cursor=cursor,
        )
        super().__init__(param)


class GetLinearInverseInstrumentsInfoReqType(
    BybitReqType[
        GetInstrumentsInfoQueryParams, GetInstrumentsInfoLinearInverseResponseData
    ]
):
    METHOD: str = "GET"
    PATH: str = "/v5/market/instruments-info"
    SHOULD_SIGN: bool = False

    def __init__(
        self,
        symbol: Optional[str] = None,
        status: Optional[str] = None,
        baseCoin: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ):
        param = GetInstrumentsInfoQueryParams(
            category="linear"
            if symbol is None or not symbol.endswith("USD")
            else "inverse",
            symbol=symbol,
            status=status,
            baseCoin=baseCoin,
            limit=limit,
            cursor=cursor,
        )
        super().__init__(param)


class GetOptionInstrumentsInfoReqType(
    BybitReqType[GetInstrumentsInfoQueryParams, GetInstrumentsInfoOptionResponseData]
):
    METHOD: str = "GET"
    PATH: str = "/v5/market/instruments-info"
    SHOULD_SIGN: bool = False

    def __init__(
        self,
        symbol: Optional[str] = None,
        status: Optional[str] = None,
        baseCoin: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ):
        param = GetInstrumentsInfoQueryParams(
            category="option",
            symbol=symbol,
            status=status,
            baseCoin=baseCoin,
            limit=limit,
            cursor=cursor,
        )
        super().__init__(param)
