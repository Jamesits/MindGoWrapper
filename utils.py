#!/usr/bin/env python3
# MindGoWrapper
# by James Swineson, 2017-06
# https://github.com/Jamesits/MindGoWrapper

def df_iter(df, seq, rank=False, ascending=True):
    '''遍历 dataframe 的每个下标，可选使用数值或者排名'''
    for f in df:
        df['rank_' + f] = df[f].rank(ascending=ascending)
    for i in seq:
        if rank:
            yield df['rank_' + i]
        else:
            yield df[i]