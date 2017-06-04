from .scheduler import Scheduler
import logging
from functools import partial

class Wrapper():
  def _mindgo_initialize(self, account):
    self.account = account
    self.log.info('_mindgo_initialize')

  def _mindgo_handle_data(self, account, data):
    self.account = account
    self.data = data
    self.log.info('_mindgo_handle_data')

  def _mindgo_before_trading_start(self, account, data):
    self.account = account
    self.data = data
    self.log.info('_mindgo_before_trading_start')

  def _mindgo_after_trading_end(self, account, data):
    self.account = account
    self.data = data
    self.log.info('_mindgo_after_trading_end')

  def __init__(self):
    # self.scheduler = Scheduler()
    # MindGo global objects
    self.account = None
    self.data = None
    self.log = logging.getLogger("MindGoWrapper")
    self.log.setLevel(logging.INFO) # seems of no use
    self.log.info('MindGoWrapper\nhttps://github.com/Jamesits/MindGoWrapper')