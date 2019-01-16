#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/1/16  上午9:04

from django import template
import json
import time


register = template.Library()


@register.filter(name='json_dumps')
def json_dumps(value):
    try:
        return json.dumps(json.loads(value), indent=4, separators=(',', ': '), ensure_ascii=False)
    except Exception:
        return value


@register.filter(name="convert_timestamp")
def convert_timestamp(value):
    return time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(int(float(value))))
