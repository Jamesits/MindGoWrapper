#!/usr/bin/env python3
# MindGoWrapper
# by James Swineson, 2017-06
# https://github.com/Jamesits/MindGoWrapper

import sys
import logging
import traceback
from .utils import detect_runtime


class Mayday():
    '''MindGoWrapper 的自定义未处理异常输出'''

    def __excepthook(self, e_type, e_value, e_traceback):
        '''Runs when there is a global uncatched exception'''
        if issubclass(e_type, KeyboardInterrupt):
            sys.__excepthook__(e_type, e_value, e_traceback)
            return
        self.log_exception((e_type, e_value, e_traceback))
        sys.__excepthook__(e_type, e_value, e_traceback)

    def log_exception(self, additional_message, exc_info):
        # Construct log string
        logstr = '''%%% Unhandled exception %%%
Date: {}, Days = {}, Ticks = {}, Additional message: {}
{}'''.format(
            self.wrapper.date.strftime("%Y-%m-%d"),
            self.wrapper.days,
            self.wrapper.ticks,
            additional_message,
            "".join(traceback.format_exception(
                exc_info[0], exc_info[1], exc_info[2])),
        )
        if detect_runtime() == 'strategy':
            # 如果在回测环境下，只能用平台提供的 log 函数
            self.wrapper.platform_apis.log.info("MindGoWrapper critical: " + logstr)
        else:
            # 否则用 logging 库
            self.log.critical(logstr)

    def __init__(self, wrapper):
        sys.excepthook = self.__excepthook
        self.wrapper = wrapper
        self.log = logging.getLogger("MindGoWrapper.Mayday")
