#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/5/30  下午5:00

VALIDATION_INFO = {
    "fail": {
        "code": "9998",
        "msg": "用户未认证",
        "success": False
    },
    "time_out": {
        "code": "9997",
        "msg": "登陆超时，请重新登陆",
        "success": False
    },
    "no_exist": {
        "success": False,
        "msg": "指定的配置文件不存在",
        "code": "9999"
    },
    "run": {
        "success": True,
        "msg": "集成自动化用例运行中",
        "code": "0001"
    }

}

