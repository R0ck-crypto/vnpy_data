"""
Event type string used in the trading platform.
"""

from vnpy.event import EVENT_TIMER  # noqa

EVENT_TICK = "eTick."
EVENT_BAR = "eBar."
EVENT_TRADE = "eTrade."
EVENT_ORDER = "eOrder."
EVENT_POSITION = "ePosition."
EVENT_ACCOUNT = "eAccount."
EVENT_QUOTE = "eQuote."
EVENT_CONTRACT = "eContract."
EVENT_LOG = "eLog"


EVENT_TICK_BINANCE = "eTick.binance"
EVENT_TRADE_BINANCE = "eTrade.binance"
EVENT_AGGTRADE_BINANCE = "eaggTrade.binance"
EVENT_BAR_BINANCE = "eBar.binance"
EVENT_DEPTH_BINANCE = "eDepth.binance"





