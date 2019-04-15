#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/4/15  下午5:16

import functools
import logging

from fastrunner.utils import parser

logger = logging.getLogger('FasterRunner')


def request_log(level):
    def wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(request, *args, **kwargs):
            msg_data = "before process request data:\n{data}".format(data=parser.format_json(request.data))
            msg_params = "before process request params:\n{params}".format(
                params=parser.format_json(request.query_params))
            if level is 'INFO':
                if request.data:
                    logger.info(msg_data)
                if request.query_params:
                    logger.info(msg_params)
            elif level is 'DEBUG':
                if request.data:
                    logger.debug(msg_data)
                if request.query_params:
                    logger.debug(msg_params)
            return func(request, *args, **kwargs)

        return inner_wrapper

    return wrapper
