# coding: utf-8
__author__ = 'chengc017'
from datetime import datetime

def objects2dicts(objects):
    if objects is None or len(objects)<1:
        return
    dicts=[]
    for obj in objects:
        dicts.append(to_json(obj,obj.__class__))
    return dicts

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        elif isinstance(v,datetime):
            d[c.name]=v.strftime('%Y-%m-%d %H:%M:%S')
        else:
            d[c.name] = v
    return d

#和 objects2dicts只是时间的展示方式不同
def objects2dicts_2(objects):
    if objects is None or len(objects)<1:
        return
    dicts=[]
    for obj in objects:
        dicts.append(to_json_2(obj,obj.__class__))
    return dicts

def to_json_2(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        elif isinstance(v,datetime):
            d[c.name]=v.strftime('%Y-%m-%d')
        else:
            d[c.name] = v
    return d

