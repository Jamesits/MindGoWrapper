from enum import Enum
from collections import Iterable

class Scheduler():
    class Unit(Enum):
        '''时间单位'''
        DAY = 0
        TICK = 1

    class Slot(Enum):
        '''在之前还是之后'''
        BEFORE = 0
        AFTER = 1

    @staticmethod
    def timeslot(position, length, unit, slot):
        '''创建一个待办事项
        position：在第 N 个单位时间处触发
        length：每隔几个单位时间重复发生
        unit：时间单位
        slot：发生在该时间的系统事件之前还是之后'''
        ret = []
        try:
            for p in position:
                ret.append({'position': p, 'length': length, 'unit': unit, 'slot': slot})
        except TypeError:
            ret = [{'position': position, 'length': length, 'unit': unit, 'slot': slot}]

        return ret

    def __init__(self):
        self.schedules = []

    def schedule(self, callback, timeslots):
        for t in timeslots:
            t['callback'] = callback
            self.schedules.append(t)
    
    def check(self, count, unit, slot):
        for s in self.schedules:
            if s['unit'] == unit and s['slot'] == slot and count % s['length'] == s['position']:
                s['callback']()