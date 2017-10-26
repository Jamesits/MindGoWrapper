#!/usr/bin/env python3
# MindGoWrapper
# by James Swineson, 2017-06
# https://github.com/Jamesits/MindGoWrapper

from .utils import detect_runtime
from .moduleproxy import ModuleProxy
p = ModuleProxy()
p.import_module((
    "atexit",
    "sys",
    "logging",
    "os",
    "platform",
    "traceback",
    "uuid",
))

class Mayday():
    '''MindGoWrapper 的自定义未处理异常输出'''

    @p.imported
    def __excepthook(self, e_type, e_value, e__traceback):
        '''Runs when there is a global uncatched exception'''
        if issubclass(e_type, KeyboardInterrupt):
            _sys.__excepthook__(e_type, e_value, e__traceback)
            return
        self.log_exception((e_type, e_value, e__traceback))
        _sys.__excepthook__(e_type, e_value, e__traceback)

    @p.imported
    def __exithook(self):
        '''Runs when program exit'''
        self.log_exception("MindGoWrapper.Mayday.log_exception.__exithook", _sys.exc_info())

    @p.imported
    def log_exception(self, additional_message, exc_info, do_callback=True):
        # Construct log string
        try:
            current_date = self.wrapper.date.strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            current_date = "Unable to get current date"
        logstr = '''%%% Unhandled exception %%% Session: {}
Date: {}, Days: {}, Ticks: {}, Additional message: {}
_os: {},Python: {},pwd: {}
{}'''.format(
            self.session_id,
            current_date,
            self.wrapper.days,
            self.wrapper.ticks,
            additional_message,
            _platform._platform(),
            _sys.version,
            _os.getcwd(),
            "".join(_traceback.format_exception(
                exc_info[0], exc_info[1], exc_info[2])),
        )
        if detect_runtime() == 'strategy':
            # 如果在回测环境下，只能用平台提供的 log 函数
            self.wrapper._platform_apis.log.info(
                "MindGoWrapper critical: " + logstr)
        else:
            # 否则用 _logging 库
            self.log.critical(logstr)
        if callable(self.log_callback):
            try:
                self.log_callback(
                    self.session_id, additional_message, exc_info, logstr)
            except:
                self.log_exception(
                    "MindGoWrapper.Mayday.log_exception.callback", _sys.exc_info(), do_callback=False)

    @p.imported
    def set_log_callback(self, func):
        self.log_callback = func

    @p.imported
    def __init__(self, wrapper, log_callback=None):
        _sys.excepthook = self.__excepthook
        self.wrapper = wrapper
        self.log = _logging.getLogger("MindGoWrapper.Mayday")
        # log_callback = function(session_id, additional_message, exc_info, log_message)
        self.log_callback = log_callback
        # random session id
        self.session_id = _uuid.uuid1()
        # register interpreter exit handler
        _atexit.register(self.__exithook)
