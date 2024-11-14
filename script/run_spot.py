from time import sleep

from vnpy_evo.event import EventEngine
from vnpy_evo.trader.engine import MainEngine
from vnpy_binance import BinanceSpotGateway
from vnpy_novastrategy import NovaStrategyApp
from vnpy_novastrategy.base import EVENT_NOVA_LOG
from vnpy_evo.trader.setting import get_settings

setting = get_settings()

def main():
    """主入口函数"""

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)


    log_engine = main_engine.get_engine("log")
    event_engine.register(EVENT_NOVA_LOG, log_engine.process_log_event)
    main_engine.write_log("注册日志事件监听")

    main_engine.add_gateway(BinanceSpotGateway)
    stg_engine = main_engine.add_app(NovaStrategyApp)
    main_engine.write_log("主引擎创建成功")

    main_engine.connect(setting, "BINANCE_SPOT")
    main_engine.write_log("连接Binance接口")
    sleep(10)

    stg_engine.init_engine()
    sleep(10)

    # 初始化所有策略
    stg_engine.init_all_strategies()
    sleep(30)
    main_engine.write_log("策略全部初始化")

    # 开启所有策略
    stg_engine.start_all_strategies()
    main_engine.write_log("策略全部启动")






if __name__ == "__main__":
    main()
