import logging
logging.basicConfig(level=logging.INFO)

from MindGoWrapper.wrapper import Wrapper
from MindGoWrapper.map import Map

config = Map({
    # 交易分频
    # 如果交易的 tick 高于需要的频率，可以在这里设定让交易以 1/n 的速度执行
    'data_handler_divider': 30,
    # 选股数量
    'security_count': 10,
    # 资金用于投资的比例
    'currency_use_percent': 0.8,
    # 每只股票最多买的股数
    'security_buy_count_limit': 10000000,
    # 择时逻辑
    'timing': Map({
        # 策略逻辑
        # 等下再设置，现在函数还没定义
        'time_selection_triggers': [],
        # 敏感度
        # 多少个策略票数会让持仓到达范围边缘
        'sensitivity': 3,
        # MACD 参数
        'macd': Map({
            'fastperiod': 12,
            'slowperiod': 26,
            'signalperiod': 9,
        }),
        # 凯利公式
        'kelly': Map({
            # 计算用的时间范围（天）
            'date_range': 140,
            # 时间窗口
            'window': 11,
        }),
    }),
    # 选股逻辑
    'selection': Map({
        # 从数据库提取的因子
        'factors': (
            'dividend_rate',
        'current_market_cap',
        'basic_pey_ear_growth_ratio',
        'total_profit_growth_ratio',
        'net_profit_growth_ratio',
        'diluted_net_asset_growth_ratio',
        'rsi',
        'vma',
        ),
        # 复合因子中每个因子的权重
        'compound_factors': (
             (-0.076890013,
                -0.211903744,
                0.450703447,
                0.43784622,
                0.443760827,
                0.45689614,
                0.194470869,
                -0.332934149,),
             (0.732930488,
            -0.522358952,
            -0.12145776,
            -0.136083851,
            -0.123607418,
            0.026704496,
            -0.093903804,
            -0.363143737,),
        ),
        # 各个复合因子的权重
        'compound_factor_weights': (0.5, 0.5),
    }),
})

w = Wrapper(globals(), config)
w.takeown()
# initialize = w._mindgo_initialize
# handle_data = w._mindgo_handle_data
# before_trading_start = w._mindgo_before_trading_start
# after_trading_end = w._mindgo_after_trading_end

