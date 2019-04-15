#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/4/15  下午4:37

import os

from celery import Celery
# set the default Django settings module for the 'celery' program.
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FasterRunner.settings')

app = Celery('FasterRunner')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
