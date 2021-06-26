#!/usr/bin/python2
# coding=utf-8

# todo: 变长数据描述

import ctypes
from collections import OrderedDict

class StructWithDefault(ctypes.Structure):
    fields_desc = []
    def __init__(self, *args, **kwargs):
        for k,v in self.__class__.defaults.items()[len(args):]:
            if k not in kwargs:
                kwargs[k] = v
        return ctypes.Structure.__init__(self, *args, **kwargs)
    def __new__(cls, *args, **kwargs):
        cls._fields_ = [ (field[0], field[1][0]) for field in cls.fields_desc ] 
        cls.defaults = OrderedDict([ (field[0], field[1][1]) for field in cls.fields_desc ])
        print(cls.__name__)
        return ctypes.Structure.__new__(cls, *args, **kwargs)

class struct_1(StructWithDefault):
    _pack_ = 4
    fields_desc = [
        ('test', (ctypes.c_uint32, 0x11332244)),
        ('c2', (ctypes.c_uint16, 0x5566)),
        ('c1', (ctypes.c_uint8,  0x77)),
        ('c3', (ctypes.c_uint16, 0x8899)),
    ]

a = struct_1(0x11220044, c1=0xcc)

print(hex(a.test))
stream = ctypes.string_at(ctypes.addressof(a), ctypes.sizeof(a))
print(stream.encode('hex'))
