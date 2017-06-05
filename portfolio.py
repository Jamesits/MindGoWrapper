#!/usr/bin/env python3
# MindGoWrapper
# by James Swineson, 2017-06
# https://github.com/Jamesits/MindGoWrapper

import logging
from .map import Map

log = logging.getLogger("MindGoWrapper.Portfolio")


class Portfolio(Map):
    '''一支股票的数据存储'''
    def __init__(self, symbol, cash_pool, initial_purchase):
        '''股票，所有参数为价格'''
        # 股票号码
        self.symbol = symbol
        # 初始现金池
        self.initial_cash_pool = cash_pool
        # 当前现金池
        self.cash_pool = cash_pool - initial_purchase
        # 当前总价值
        self.has_value = 0
        # 持股成本
        self.cost = 0
        # 目标持股价值
        self.object_value = initial_purchase
        # 是否为等待卖空扔掉状态
        self.removed = False
        # 未完成的交易
        self.orders = []
        log.debug('新股票：{} 初始持仓 {} 元'.format(
            self.symbol, self.initial_cash_pool))

    def set_new_object(self, new_object_value):
        '''设置新的目标持仓'''
        self.object_value = new_object_value
        log.debug('新持仓目标：{} {} 元'.format(self.symbol, self.object_value))

    def new_finished_order(self, order, current_price):
        '''产生新订单，重新计算相关参数
        order：一个 order 对象
        current_price：成交时股票单价'''
        if order.symbol == self.symbol:
            price_delta = order.filled * current_price - order.commission
            if order.filled < 0:
                price_delta -= order.tax
            self.cash_pool += price_delta
            log.debug('新订单：{} {} 股，价格变化 {} 元，当前现金池 {} 元，持仓 {} 元'.format(
                self.symbol, order.filled, price_delta, self.cash_pool, self.object_value))
        else:
            log.error('股票代码 {} 和订单中的股票代码 {} 不符'.format(
                self.symbol, order.symbol))

    def prepare_remove(self):
        '''准备卖空该股票'''
        self.object_value = 0
        self.removed = True
