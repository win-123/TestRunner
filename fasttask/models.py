from django.db import models

# Create your models here.
from fastrunner.models import Project
from fastuser.models import BaseTable


class Schedule(BaseTable):
    """
    定时任务信息表
    """
    send_strategy = (
        (1, "不发送结果"),
        (2, "失败后发送"),
        (3, "不管怎样都发送结果")
    )

    triggers_type = (
        (1, "始终发送"),
        (2, "仅失败发送"),
        (3, "从不发送"),
    )

    name = models.CharField("任务名称", unique=True, null=False, max_length=100)
    identity = models.CharField("任务ID", unique=True, null=False, max_length=100)
    send_type = models.IntegerField("发送策略", choices=send_strategy, default=3)
    config = models.TextField("任务分配", null=False)
    receiver = models.CharField("接受人", null=True, max_length=2048)
    copy = models.CharField("抄送人", null=True, max_length=2048)
    status = models.BooleanField("状态", default=True)
    project = models.ForeignKey(Project, verbose_name='所属项目', null=False, on_delete=models.CASCADE)

    # desc = models.CharField("简要介绍", max_length=100, null=False)
    # triggers = models.IntegerField("触发器", choices=triggers_type, default=1)
    # crontab = models.CharField("时间配置", max_length=100, null=False)
    # creator = models.CharField("创建者", max_length=50)

    class Meta:
        verbose_name = "定时任务"
        db_table = "Schedule"
