from vnpy.trader.object import *
from enum import Enum
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass
class BinanceTicker:
    """
    Binance 24小时Ticker数据结构
    官方文档: https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics
    """
    # 事件类型和时间
    event_type: str  # 'e': 事件类型，例如 "24hrTicker"
    event_time: datetime  # 'E': 事件时间

    # 交易对信息
    symbol: str  # 's': 交易对，例如 "ETHUSDT"

    # 价格变动信息
    price_change: Decimal  # 'p': 24小时价格变动
    price_change_percent: Decimal  # 'P': 24小时价格变动百分比
    weighted_avg_price: Decimal  # 'w': 加权平均价格

    # 当前价格信息
    last_price: Decimal  # 'c': 最新价格
    last_quantity: Decimal  # 'Q': 最新成交量

    # 24小时统计
    open_price: Decimal  # 'o': 24小时开盘价
    high_price: Decimal  # 'h': 24小时最高价
    low_price: Decimal  # 'l': 24小时最低价
    total_volume: Decimal  # 'v': 24小时成交量
    total_quote_volume: Decimal  # 'q': 24小时成交额(计价币种)

    # 统计周期
    statistics_open_time: datetime  # 'O': 统计开始时间
    statistics_close_time: datetime  # 'C': 统计结束时间

    # 成交信息
    first_trade_id: int  # 'F': 第一笔成交ID
    last_trade_id: int  # 'L': 最后一笔成交ID
    trade_count: int  # 'n': 成交笔数

    @classmethod
    def from_dict(cls, data: dict) -> 'BinanceTicker':
        """
        从Binance WebSocket推送的字典数据创建Ticker对象
        """
        return cls(
            event_type=data['e'],
            event_time=datetime.fromtimestamp(data['E'] / 1000),
            symbol=data['s'],
            price_change=Decimal(data['p']),
            price_change_percent=Decimal(data['P']),
            weighted_avg_price=Decimal(data['w']),
            last_price=Decimal(data['c']),
            last_quantity=Decimal(data['Q']),
            open_price=Decimal(data['o']),
            high_price=Decimal(data['h']),
            low_price=Decimal(data['l']),
            total_volume=Decimal(data['v']),
            total_quote_volume=Decimal(data['q']),
            statistics_open_time=datetime.fromtimestamp(data['O'] / 1000),
            statistics_close_time=datetime.fromtimestamp(data['C'] / 1000),
            first_trade_id=int(data['F']),
            last_trade_id=int(data['L']),
            trade_count=int(data['n'])
        )

    def to_dict(self) -> dict:
        """
        将Ticker对象转换为字典格式
        """
        return {
            'event_type': self.event_type,
            'event_time': int(self.event_time.timestamp() * 1000),
            'symbol': self.symbol,
            'price_change': str(self.price_change),
            'price_change_percent': str(self.price_change_percent),
            'weighted_avg_price': str(self.weighted_avg_price),
            'last_price': str(self.last_price),
            'last_quantity': str(self.last_quantity),
            'open_price': str(self.open_price),
            'high_price': str(self.high_price),
            'low_price': str(self.low_price),
            'total_volume': str(self.total_volume),
            'total_quote_volume': str(self.total_quote_volume),
            'statistics_open_time': int(self.statistics_open_time.timestamp() * 1000),
            'statistics_close_time': int(self.statistics_close_time.timestamp() * 1000),
            'first_trade_id': self.first_trade_id,
            'last_trade_id': self.last_trade_id,
            'trade_count': self.trade_count
        }


class TradeExecutionType(str, Enum):
    """
    交易执行类型
    """
    MARKET = "MARKET"  # 市价单成交
    LIMIT = "LIMIT"  # 限价单成交
    UNKNOWN = "UNKNOWN"  # 未知类型


@dataclass
class BinanceTrade:
    """
    Binance 逐笔成交数据结构
    官方文档: https://binance-docs.github.io/apidocs/spot/en/#trade-streams
    """
    # 事件信息
    event_type: str  # 'e': 事件类型，例如 "trade"
    event_time: datetime  # 'E': 事件时间

    # 交易信息
    trade_time: datetime  # 'T': 成交时间
    symbol: str  # 's': 交易对
    trade_id: int  # 't': 交易ID
    price: Decimal  # 'p': 成交价格
    quantity: Decimal  # 'q': 成交数量
    execution_type: TradeExecutionType  # 'X': 执行类型（MARKET, LIMIT等）
    is_buyer_maker: bool  # 'm': 是否是买方为maker

    @classmethod
    def from_dict(cls, data: dict) -> 'BinanceTrade':
        """
        从Binance WebSocket推送的字典数据创建Trade对象
        """
        return cls(
            event_type=data['e'],
            event_time=datetime.fromtimestamp(data['E'] / 1000),
            trade_time=datetime.fromtimestamp(data['T'] / 1000),
            symbol=data['s'],
            trade_id=int(data['t']),
            price=Decimal(data['p']),
            quantity=Decimal(data['q']),
            execution_type=TradeExecutionType(data.get('X', 'UNKNOWN')),
            is_buyer_maker=bool(data['m'])
        )

    def to_dict(self) -> dict:
        """
        将Trade对象转换为字典格式
        """
        return {
            'event_type': self.event_type,
            'event_time': int(self.event_time.timestamp() * 1000),
            'trade_time': int(self.trade_time.timestamp() * 1000),
            'symbol': self.symbol,
            'trade_id': self.trade_id,
            'price': str(self.price),
            'quantity': str(self.quantity),
            'execution_type': self.execution_type.value,
            'is_buyer_maker': self.is_buyer_maker
        }


@dataclass
class BinanceAggregatedTrade:
    """
    Binance 聚合交易数据结构
    官方文档: https://binance-docs.github.io/apidocs/spot/en/#aggregate-trade-streams
    """
    event_type: str  # 'e': 事件类型，固定为 "aggTrade"
    event_time: datetime  # 'E': 事件时间
    agg_trade_id: int  # 'a': 聚合交易ID
    symbol: str  # 's': 交易对
    price: Decimal  # 'p': 成交价格
    quantity: Decimal  # 'q': 成交数量
    first_trade_id: int  # 'f': 被聚合的第一个交易ID
    last_trade_id: int  # 'l': 被聚合的最后一个交易ID
    trade_time: datetime  # 'T': 成交时间
    is_buyer_maker: bool  # 'm': 是否是买方挂单成交

    @classmethod
    def from_dict(cls, data: dict) -> 'AggregatedTrade':
        """
        从Binance WebSocket推送的字典数据创建AggregatedTrade对象
        """
        return cls(
            event_type=data['e'],
            event_time=datetime.fromtimestamp(data['E'] / 1000),
            agg_trade_id=int(data['a']),
            symbol=data['s'],
            price=Decimal(data['p']),
            quantity=Decimal(data['q']),
            first_trade_id=int(data['f']),
            last_trade_id=int(data['l']),
            trade_time=datetime.fromtimestamp(data['T'] / 1000),
            is_buyer_maker=bool(data['m'])
        )

    def to_dict(self) -> dict:
        """
        将AggregatedTrade对象转换为字典格式
        """
        return {
            'e': self.event_type,
            'E': int(self.event_time.timestamp() * 1000),
            'a': self.agg_trade_id,
            's': self.symbol,
            'p': str(self.price),
            'q': str(self.quantity),
            'f': self.first_trade_id,
            'l': self.last_trade_id,
            'T': int(self.trade_time.timestamp() * 1000),
            'm': self.is_buyer_maker
        }


@dataclass
class BinanceKlineData:
    """
    Binance K线数据结构
    官方文档: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-streams
    """
    event_type: str  # 'e': 事件类型，固定为 "kline"
    event_time: datetime  # 'E': 事件时间
    symbol: str  # 's': 交易对
    start_time: datetime  # 'k.t': K线开始时间
    end_time: datetime  # 'k.T': K线结束时间
    interval: str  # 'k.i': K线间隔
    first_trade_id: int  # 'k.f': 第一笔成交ID
    last_trade_id: int  # 'k.L': 最后一笔成交ID
    open_price: Decimal  # 'k.o': 开盘价
    close_price: Decimal  # 'k.c': 收盘价
    high_price: Decimal  # 'k.h': 最高价
    low_price: Decimal  # 'k.l': 最低价
    volume: Decimal  # 'k.v': 成交量
    trades_count: int  # 'k.n': 成交笔数
    is_closed: bool  # 'k.x': K线是否完结
    quote_volume: Decimal  # 'k.q': 成交额
    taker_volume: Decimal  # 'k.V': 主动买入成交量
    taker_quote_volume: Decimal  # 'k.Q': 主动买入成交额

    @classmethod
    def from_dict(cls, data: dict) -> 'KlineData':
        """
        从Binance WebSocket推送的字典数据创建KlineData对象
        """
        k = data['k']
        return cls(
            event_type=data['e'],
            event_time=datetime.fromtimestamp(data['E'] / 1000),
            symbol=data['s'],
            start_time=datetime.fromtimestamp(k['t'] / 1000),
            end_time=datetime.fromtimestamp(k['T'] / 1000),
            interval=k['i'],
            first_trade_id=int(k['f']),
            last_trade_id=int(k['L']),
            open_price=Decimal(k['o']),
            close_price=Decimal(k['c']),
            high_price=Decimal(k['h']),
            low_price=Decimal(k['l']),
            volume=Decimal(k['v']),
            trades_count=int(k['n']),
            is_closed=bool(k['x']),
            quote_volume=Decimal(k['q']),
            taker_volume=Decimal(k['V']),
            taker_quote_volume=Decimal(k['Q'])
        )

    def to_dict(self) -> dict:
        """
        将KlineData对象转换为字典格式
        """
        return {
            'e': self.event_type,
            'E': int(self.event_time.timestamp() * 1000),
            's': self.symbol,
            'k': {
                't': int(self.start_time.timestamp() * 1000),
                'T': int(self.end_time.timestamp() * 1000),
                's': self.symbol,
                'i': self.interval,
                'f': self.first_trade_id,
                'L': self.last_trade_id,
                'o': str(self.open_price),
                'c': str(self.close_price),
                'h': str(self.high_price),
                'l': str(self.low_price),
                'v': str(self.volume),
                'n': self.trades_count,
                'x': self.is_closed,
                'q': str(self.quote_volume),
                'V': str(self.taker_volume),
                'Q': str(self.taker_quote_volume),
                'B': '0'
            }
        }
