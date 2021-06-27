#!/usr/bin/python2
# coding=utf-8

import ctypes
from collections import OrderedDict
from functools import partial

def raw(v):
    return ctypes.string_at(ctypes.addressof(v), ctypes.sizeof(v))

def rawhex(v):
    return raw(v).encode('hex')

class StructWithDefault(ctypes.Structure):
    fields_desc = []

    def __init__(self, *args, **kwargs):
        for k,v in self.__class__.defaults.items()[len(args):]:
            if k not in kwargs:
                kwargs[k] = v
        return ctypes.Structure.__init__(self, *args, **kwargs)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_fields_') or not cls._fields_:
            cls._fields_ = [ (field[0], field[1][0]) for field in cls.fields_desc ] 
        if not hasattr(cls, 'defaults') or not cls.defaults:
            cls.defaults = OrderedDict([ (field[0], field[1][1]) for field in cls.fields_desc ])
        return ctypes.Structure.__new__(cls, *args, **kwargs)

class StructSerial(object):
    def __init__(self, fields):
        self.__dict__['attr'] = OrderedDict()
        for k, v in fields:
            self.attr[k] = v()
    def __getattr__(self, name):
        if name in self.attr:
            return self.attr[name]
        else:
            return None
    def __setattr__(self, key, value):
        if key in self.attr:
            setattr(self.attr, key, value)
    def __iter__(self):
        return iter(self.attr.copy())
    def raw(self):
        result = ''
        for k in self:
            v = getattr(self, k)
            result += ctypes.string_at(ctypes.addressof(v), ctypes.sizeof(v))
        return result

def dyn_str(str_content):
    dyn_serial = StructSerial([
        ('len', partial(ctypes.c_uint32, len(str_content))),
        ('content', partial(ctypes.create_string_buffer, str_content, len(str_content))),
        ])
    return dyn_serial.raw()

def test():
    """
        example
    """

    # 构建字段类序
    class struct_1(StructWithDefault):
        _pack_ = 4
        fields_desc = [
            ('test', (ctypes.c_uint32, 0x11332244)),
            ('c2', (ctypes.c_uint16, 0x5566)),
            ('c1', (ctypes.c_uint8,  0x77)),
            ('c3', (ctypes.c_uint16, 0x8899)),
        ]
    
    # 构建数据包结构
    # 变长类型放在这一层解决
    s = StructSerial([
            ('f1', struct_1),
            ('f2', partial(struct_1, 0x66aaaa55, c3=0xbbdd)),
        ])

    s.f1.test = 0x99887766
    print(hex(s.f1.test))
    print(raw(s.f2).encode('hex'))
    print(s.raw().encode('hex'))
    a = struct_1(0x11220044, c1=0xcc)
    print(hex(a.test))
    print(raw(a).encode('hex'))

if __name__ == '__main__':
    test()
