#!/usr/bin/env python3
# MindGoWrapper
# by James Swineson, 2017-06
# https://github.com/Jamesits/MindGoWrapper

import sys
import logging


class Mayday():
    '''MindGoWrapper 的自定义未处理异常输出'''

    def __excepthook(self, e_type, e_value, e_traceback):
        # Construct log string
        logstr = '''%%% Unhandled exception %%%
        Date: {}, Days = {}, Ticks = {}
        Exception: {} {}
        Traceback: 
        {}
        '''.format(
            self.wrapper.date.strftime("%Y-%m-%d"),
            self.wrapper.days,
            self.wrapper.ticks,
            e_type,
            e_value,
            e_traceback,
        )
        # Output twice using logging module and platform's log function
        self.log.error(logstr)
        self.wrapper.platform_apis.log.info(logstr)
        # Run the original excepthook
        sys.__excepthook__(e_type, e_value, e_traceback)

    def __init__(self, wrapper):
        sys.excepthook = self.__excepthook
        self.wrapper = wrapper
        self.log = logging.getLogger("MindGoWrapper.Mayday")
