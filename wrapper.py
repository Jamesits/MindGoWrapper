from .scheduler import Scheduler
from .portfolio import Portfolio
import logging
from functools import partial

class Wrapper():
  def update_portfolios_data(self):
    '''更新各股票的数据'''
    for key, value in account.positions:
      if key in self.portfolios:
        self.portfolios[key].has_amount = value.total_amount
        self.portfolios[key].value = value.position_value
      else:
        self.portfolios[key] = Portfolio(key)


  def _mindgo_initialize(self, account):
    self.account = account
    self.log.debug('_mindgo_initialize')
    print('init')

  def _mindgo_handle_data(self, account, data):
    self.account = account
    self.data = data
    self.log.debug('_mindgo_handle_data')

  def _mindgo_before_trading_start(self, account, data):
    self.account = account
    self.data = data
    self.log.debug('_mindgo_before_trading_start')

  def _mindgo_after_trading_end(self, account, data):
    self.account = account
    self.data = data
    self.log.debug('_mindgo_after_trading_end')

  def __init__(self, platform_apis, config):
    # self.scheduler = Scheduler()
    self.platform_apis = platform_apis
    self.config = config
    self.account = None
    self.data = None
    self.portfolios = {}
    self.log = logging.getLogger("MindGoWrapper")
    self.log.setLevel(logging.INFO) # seems of no use
    self.log.info('https://github.com/Jamesits/MindGoWrapper')

  def takeown(self):
    self.platform_apis['initialize'] = self._mindgo_initialize
    self.platform_apis['handle_data'] = self._mindgo_handle_data
    self.platform_apis['before_trading_start'] = self._mindgo_before_trading_start
    self.platform_apis['after_trading_end'] = self._mindgo_after_trading_end
    self.log.debug('takeown finished')