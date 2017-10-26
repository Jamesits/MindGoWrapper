#!/usr/bin/env python3
# MindGoWrapper
# by James Swineson, 2017-06
# https://github.com/Jamesits/MindGoWrapper

from .moduleproxy import ModuleProxy
p = ModuleProxy()
p.import_module("sys")


def df_iter(df, seq, rank=False, ascending=True):
    '''遍历 dataframe 的每个下标，可选使用数值或者排名'''
    for f in df:
        df['rank_' + f] = df[f].rank(ascending=ascending)
    for i in seq:
        if rank:
            yield df['rank_' + i]
        else:
            yield df[i]


@p.imported
def detect_runtime():
    '''识别当前在哪种运行环境下
    如果在“我的策略”当中回测，返回 'strategy'
    如果在“我的研究”中的 Jupyter 环境里回测，返回 'research'
    无法识别则返回 'unknown'
    '''
    if 'ipykernel' in sys.modules:
        return 'research'
    elif 'IPython' in sys.modules:
        return 'strategy'
    else:
        return 'unknown'
