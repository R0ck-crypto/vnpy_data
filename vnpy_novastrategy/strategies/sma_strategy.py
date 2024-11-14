from vnpy.trader.object import TradeData
from vnpy_evo.trader.object import BinanceSpotDepthData, BinanceDepthData
from vnpy_novastrategy import (
    StrategyTemplate,
    BarData,
    TickData,
   OrderData,
    ArrayManager,
    datetime
)


class SmaStrategy(StrategyTemplate):
    """Double SMA (simple moving average) strategy"""

    author: str = "VeighNa Global"
    subscribe_ticker = False
    subscribe_trade = False
    subscribe_depth = True
    depth_level = 5
    subscribe_kline = False


    def on_init(self) -> None:
        """Callback when strategy is inited"""
        self.trading_symbol: str = self.vt_symbols[0]

        self.bar_dt: datetime = None
        self.has_executed_buy = False
        self.has_executed_sell = False
        self.am: ArrayManager = ArrayManager()
        self.write_log("Strategy is inited.")


    def on_start(self) -> None:
        """Callback when strategy is started"""
        self.write_log("Strategy is started.")

    def on_stop(self) -> None:
        """Callback when strategy is stoped"""
        self.write_log("Strategy is stopped.")


    def on_depth(self, depth) -> None:
        """Callback of depth data update"""
        # self.write_log("depth data update")
        # self.write_log(depth)


        if isinstance(depth, BinanceSpotDepthData) and not self.has_executed_buy and self.trading:
            self.buy(f'{depth.symbol}.BINANCE', depth.bids[0][0], 0.002)
            self.write_log(f"Bought spot at {depth.bids[0][0]}")
            self.has_executed_buy = True


        if isinstance(depth, BinanceDepthData) and not self.has_executed_sell and self.trading:
            self.short(f'{depth.symbol}.BINANCE', depth.asks[0][0], 0.002)
            self.write_log(f"Sold derivatives at {depth.asks[0][0]}")
            self.has_executed_sell = True


    def on_trade(self, trade: TradeData) -> None:
        self.write_log(trade)

    def on_order(self, order:OrderData):
        self.write_log(order)


    def on_order(self, order: OrderData) -> None:
        """Callback of order update"""
        pass
