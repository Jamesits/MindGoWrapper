class Portfolio():
    def __init__(self, symbol):
        # 股票号码
        self.symbol = symbol
        # 现金池
        self.cash_pool = 0
        # 允许买入的最大总价格
        self.total_price_limit = 0
        # 当前持股数
        self.has_amount = 0
        # 当前总价值
        self.value = 0
        # 目标持股数
        self.object_amount = 0

    def try_purchase(object_amount=None):
        if object_amount != None:
            self.object_amount = object_amount
        # 尝试调仓
        order_target(symbol, target)
        