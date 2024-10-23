from enum import Enum

from vnpy.trader.constant import (
    Direction,
    Offset,
    Status,
    Product,
    OrderType,
    OptionType,
    Currency,
    Interval,
)


class Exchange(Enum):
    """
    Exchange.
    """
    # Crypto
    BINANCE = "BINANCE"
    OKX = "OKX"
    BYBIT = "BYBIT"
    BTSE = "BTSE"
    DERIBIT = "DERIBIT"

    # Global
    OTC = "OTC"

    # Special Function
    LOCAL = "LOCAL"  # For local generated data





class EnumX(Enum):

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def has_name(cls, key):
        return key in cls._member_map_


class Market(EnumX):
    CRYPTO = "crypto"
    CRYPTO_CONTRACTS = "crypto_contracts"
    CN_STOCK = "cn_stock"
    CN_FUTURE = "cn_future"
    CN_INDEX = "cn_index"
