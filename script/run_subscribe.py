import time

from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.object import TickSubscribeRequest, KlineSubscribeRequest, TradeSubscribeRequest, \
    AggTradeSubscribeRequest
from vnpy_evo.trader.engine import MainEngine
from vnpy_evo.trader.event import EVENT_LOG
from vnpy_binance import BinanceLinearGateway
from vnpy_evo.event import EventEngine
from vnpy_evo.trader.setting import get_settings



setting = get_settings()

def run_subsribe():
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    log_engine = main_engine.get_engine("log")
    event_engine.register(EVENT_LOG, log_engine.process_log_event)
    main_engine.write_log("注册日志事件监听")


    main_engine.add_gateway(BinanceLinearGateway)
    main_engine.connect(setting, "BINANCE_LINEAR")

    time.sleep(5)

    # Subscribe to tick data
    tick_req = TickSubscribeRequest(
        symbols=["BTCUSDT","ETHUSDT"],
        exchange=Exchange.BINANCE,
    )
    main_engine.subscribe(tick_req, "BINANCE_LINEAR")

    # Subscribe to kline data
    kline_req = KlineSubscribeRequest(
        symbols=["BTCUSDT","ETHUSDT"],
        exchange=Exchange.BINANCE,
        interval=Interval.MINUTE
    )
    main_engine.subscribe(kline_req, "BINANCE_LINEAR")

    # Subscribe to trade data
    trade_req = TradeSubscribeRequest(
        symbols=["BTCUSDT","ETHUSDT"],
        exchange=Exchange.BINANCE
    )
    main_engine.subscribe(trade_req, "BINANCE_LINEAR")

    aggtrade_req = AggTradeSubscribeRequest(
        symbols=["BTCUSDT","ETHUSDT"],
        exchange=Exchange.BINANCE
    )
    main_engine.subscribe(aggtrade_req, "BINANCE_LINEAR")


    while True:
        pass


if __name__ == '__main__':
    run_subsribe()