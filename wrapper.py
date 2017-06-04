from .scheduler import Scheduler
import logging

class Wrapper():
  def _mindgo_initialize(self, account):
    self.account = account
    self.log.debug('_mindgo_initialize')

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

  def __init__(self):
    # self.scheduler = Scheduler()
    # MindGo global objects
    self.account = None
    self.data = None
    self.log = logging.getLogger("MindGoWrapper")
    self.log.setLevel(logging.DEBUG)

  def takeown(self):
    print('MindGoWrapper\nhttps://github.com/Jamesits/MindGoWrapper')
    # takeown all MindGo callback functions
    global initialize
    global handle_data
    global before_trading_start
    global after_trading_end
    initialize = self._mindgo_initialize
    handle_data = self._mindgo_handle_data
    before_trading_start = self.before_trading_start
    after_trading_end = self.after_trading_end
