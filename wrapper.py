from .scheduler import Scheduler
from .portfolio import Portfolio
import logging
from functools import partial
from .map import Map

class Wrapper():
  '''MindGo 平台 Wrapper。回测中使用方法：
  w = Wrapper(globals(), config)
  w.takeown()
  '''
  def create_portfolio(self, symbol, share_pool=True):
    '''准备给某支股票建仓'''
    self.portfolios[symbol] = Portfolio(symbol)
    if share_pool:
      # 现金池：当前总资产均分给当前选股数量
      self.portfolios[symbol].cash_pool = self.platform_apis.account.portfolio_value / self.config.security_count * self.config.currency_use_percent
      # 持股总价值上限：不超过现金池均分
      self.portfolios[symbol].total_price_limit = self.portfolios[symbol].cash_pool
      # 初始建仓：现金池百分比
      self.portfolios[symbol].object_value = self.portfolios[symbol].cash_pool * self.config.timing.initial_purchase

  def remove_portfolio(self, symbol):
    '''准备卖光某支股票'''
    try:
      self.portfolios[symbol].object_value = 0
      self.portfolios[symbol].removed = True
    except KeyError:
      self.log.warn("尝试卖空无仓位信息的股票：{}".format(symbol))

  def set_portfolios(self, symbols):
    '''批量更新选股信息'''
    for s in symbols:
      if s not in symbols:
        self.create_portfolio(s)
    for s in self.portfolios:
      if s not in symbols:
        self.remove_portfolio(s)

  def _update_portfolios_data(self):
    '''更新各股票的数据'''
    for key, value in self.account.positions:
      if key not in self.portfolios:
        self.log.warn("MindGoWrapper 股票信息失去同步，正在重建信息：{}".format(key))
        self.create_portfolio(key, share_pool=False)
      self.portfolios[key].has_value = value.position_value
    for key, value in self.portfolios:
      if value.has_value == 0 and value.removed:
        del self.portfolios[key]

  def _try_purchases(self):
    '''尝试调仓'''
    for key, value in self.portfolios:
      callback = partial(self.platform_apis.order_target_value, key)
      value.try_purchase(callback)

  def _mindgo_initialize(self, account):
    '''在回测平台初始化时运行'''
    self.account = account
    self.log.debug('_mindgo_initialize')
    self.date = self.account.start_date

  def _mindgo_handle_data(self, account, data):
    '''每个交易 tick 运行一次'''
    self.account = account
    self.data = data
    self.ticks += 1
    self.date = self.platform_apis.get_datetime()
    self.log.debug('_mindgo_handle_data')
    self.scheduler.check(self.days, Scheduler.Unit.TICK, Scheduler.Slot.BEFORE)
    self._update_portfolios_data()
    self._try_purchases()
    self.scheduler.check(self.days, Scheduler.Unit.TICK, Scheduler.Slot.AFTER)

  def _mindgo_before_trading_start(self, account, data):
    '''每个交易日之前运行'''
    self.account = account
    self.data = data
    self.days += 1
    self.log.debug('_mindgo_before_trading_start')
    self.scheduler.check(self.days, Scheduler.Unit.DAY, Scheduler.Slot.BEFORE)

  def _mindgo_after_trading_end(self, account, data):
    '''每个交易日结束后运行'''
    self.account = account
    self.data = data
    self.log.debug('_mindgo_after_trading_end')
    self.scheduler.check(self.days, Scheduler.Unit.DAY, Scheduler.Slot.AFTER)

  def __init__(self):
    '''Wrapper 对象初始化'''
    self.scheduler = Scheduler()
    # 一个可读写的全局变量字典
    self.callbacks = None
    # 一个只读的全局变量字典（Map 类型）
    self.platform_apis = None
    # 全局配置
    self.config = None
    # MindGo 平台给的公共对象
    self.account = None
    self.data = None
    # 当前持股情况
    self.portfolios = {}
    # 日期计数器
    self.ticks = -1
    self.days = -1
    self.date = None
    # 日志工具
    self.log = logging.getLogger("MindGoWrapper")
    self.log.setLevel(logging.INFO)
    self.log.info('https://github.com/Jamesits/MindGoWrapper')

  def takeown(self, platform_apis, config):
    '''劫持 MindGo 平台的回测回调函数，自动调用当前 Wrapper 对象的相应函数，获得回测控制权。
    platform_apis 参数为回测环境的 globals() 返回值
    config 是一个 Map 对象，保存全局配置'''
    # 一个可读写的全局变量字典
    self.callbacks = platform_apis
    # 一个只读的全局变量字典
    self.platform_apis = Map(platform_apis)
    # 全局配置
    self.config = config

    self.callbacks['initialize'] = self._mindgo_initialize
    self.callbacks['handle_data'] = self._mindgo_handle_data
    self.callbacks['before_trading_start'] = self._mindgo_before_trading_start
    self.callbacks['after_trading_end'] = self._mindgo_after_trading_end

    self.log.debug('takeown finished')