#!/usr/bin/env python3
# MindGoWrapper
# by James Swineson, 2017-06
# https://github.com/Jamesits/MindGoWrapper

import logging
from functools import partial
import datetime
from .scheduler import Scheduler
from .portfolio import Portfolio
from .mayday import Mayday
from .map import Map


class Wrapper():
    '''MindGo 平台 Wrapper。'''

    welcome_string = 'https://github.com/Jamesits/MindGoWrapper'
    ################################
    # 获取数据

    def get_current_price(self, symbol):
        '''获取当前价格'''
        return self.data.current(symbol)[symbol].open

    def is_paused(self, symbol):
        '''是否涨停或跌停'''
        return self.data.current(symbol)[symbol].is_paused

    ################################
    # 操作股票

    def create_portfolio(self, symbol):
        '''准备给某支股票建仓'''
        self.portfolios[symbol] = Portfolio(
            symbol,
            self.account.portfolio_value / self.config.security_count *
            self.config.currency_use_percent,
            self.account.portfolio_value / self.config.security_count *
            self.config.currency_use_percent * self.config.purchase.initial_purchase
        )

    def remove_portfolio(self, symbol):
        '''准备卖光某支股票'''
        try:
            self.portfolios[symbol].prepare_remove()
        except KeyError:
            self.log.error("尝试卖空无仓位信息的股票：{}".format(symbol))

    def get_portfolio_detail(self, symbol):
        try:
            return self.portfolios[symbol]
        except KeyError:
            self.log.error("尝试读取无仓位信息的股票：{}".format(symbol))

    def update_portfolio_object_value(self, symbol, new_object_value):
        '''更新某支股票的目标持仓'''
        try:
            self.portfolios[symbol].set_new_object(new_object_value)
            self.log.debug("股票 {} 目标持仓更新为 {} 元".format(
                symbol, new_object_value))
        except KeyError:
            self.log.error("尝试更新无仓位信息的股票：{}".format(symbol))

    def set_portfolios(self, symbols):
        '''批量更新选股信息'''
        for s in symbols:
            if s not in self.portfolios:
                self.create_portfolio(s)
        for s in self.portfolios:
            if s not in symbols:
                self.remove_portfolio(s)

    def _update_portfolios_data(self):
        '''更新各股票的数据'''
        for symbol, position in self.account.positions.items():
            if symbol not in self.portfolios:
                self.log.warn("股票 {} 信息失去同步，正在重建信息……".format(symbol))
                self.create_portfolio(symbol, share_pool=False)
            self.portfolios[symbol].has_value = position.position_value
            self.portfolios[symbol].cost = position.cost_basis
        symbols_to_be_deleted = []
        for symbol, portfolio in self.portfolios.items():
            if portfolio.has_value == 0 and portfolio.removed:
                symbols_to_be_deleted.append(symbol)
        for symbol in symbols_to_be_deleted:
            del self.portfolios[symbol]

    def _try_purchases(self):
        '''尝试调仓'''
        for symbol, portfolio in self.portfolios.items():
            object_value = portfolio.object_value
            # 不能做空
            if object_value < 0:
                object_value = 0
            if not (self.is_paused(symbol) or object_value == portfolio.has_value):
                id = self.platform_apis.order_target_value(
                    symbol, object_value)
                portfolio.orders.append(id)

    def _monitor_orders(self):
        '''监视订单完成情况，订单一旦完成就更新个股信息'''
        for symbol, portfolio in self.portfolios.items():
            open_order_objs = self.platform_apis.get_open_orders(symbol)
            open_orders = [x.id for x in open_order_objs]
            if len(open_orders) > 0:
                for order_id in portfolio.orders:
                    if order_id not in open_orders:
                        order = self.platform_apis.get_order(order_id)
                        if order != None:
                            portfolio.new_finished_order(
                                order, self.get_current_price(symbol))
                            portfolio.orders.remove(order_id)
                        else:
                            self.log.error('无法获取订单 {}，当前未完成订单：{}'.format(
                                order_id, open_orders))

    ################################
    # MindGo 平台相关

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
        self.scheduler.check(
            self.ticks, Scheduler.Unit.TICK, Scheduler.Slot.BEFORE)
        self._update_portfolios_data()
        self._try_purchases()
        self._monitor_orders()
        self.scheduler.check(
            self.ticks, Scheduler.Unit.TICK, Scheduler.Slot.AFTER)

    def _mindgo_before_trading_start(self, account, data):
        '''每个交易日之前运行'''
        self.account = account
        self.data = data
        self.days += 1
        self.log.debug('_mindgo_before_trading_start')
        self.scheduler.check(self.days, Scheduler.Unit.DAY,
                             Scheduler.Slot.BEFORE)

    def _mindgo_after_trading_end(self, account, data):
        '''每个交易日结束后运行'''
        self.account = account
        self.data = data
        self.log.debug('_mindgo_after_trading_end')
        self.scheduler.check(self.days, Scheduler.Unit.DAY,
                             Scheduler.Slot.AFTER)

    def __init__(self):
        '''Wrapper 对象初始化'''
        # 定时任务管理
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
        # 定时任务计数器
        self.ticks = -1
        self.days = -1
        # 回测日期
        self.date = datetime.datetime.now()
        # 日志
        self.log = logging.getLogger("MindGoWrapper")

        # 异常处理拦截
        self.mayday = Mayday()

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

        self.log.info(welcome_string)
        self.platform_apis.log.info(welcome_string)
        self.log.debug('takeown finished')
