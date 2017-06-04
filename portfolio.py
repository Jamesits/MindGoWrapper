class Portfolio():
    def __init__(self, symbol):
        # 股票号码
        self.symbol = symbol
        # 现金池
        self.cash_pool = 0
        # 允许买入的最大总价格
        self.total_price_limit = 0
        # 当前总价值
        self.has_value = 0
        # 目标持股价值
        self.object_value = 0
        # 是否为等待空仓状态
        self.removed = False

    def try_purchase(purchase_callback, object_value=None):
        '''尝试调仓
        purchase_callback(value)：按持仓价格调仓的函数
        object_value：新的目标持仓（可选）
        '''
        if object_value != None:
            self.object_value = object_value
        # 尝试调仓
        purchase_callback(target)
        