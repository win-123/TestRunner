from django.db import models

# Create your models here.
from fastuser.models import BaseTable


class Project(BaseTable):
    """
    项目信息表
    """
    name = models.CharField("项目名称", unique=True, null=False, max_length=100)
    desc = models.CharField("简要介绍", max_length=100, null=False)
    responsible = models.CharField("创建人", max_length=20, null=False)

    class Meta:
        verbose_name = "项目信息"
        db_table = "Project"


class Debugtalk(models.Model):
    """
    驱动文件表
    """
    code = models.TextField("python代码", default="# write you code", null=False)
    project = models.OneToOneField(to=Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "驱动库"
        db_table = "Debugtalk"


class Config(BaseTable):
    """
    环境信息表
    """

    name = models.CharField("环境名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    base_url = models.CharField("请求地址", null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "环境信息"
        db_table = "Config"


class API(BaseTable):
    """
    API信息表
    """

    name = models.CharField("接口名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=200)
    method = models.CharField("请求方式", null=False, max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relation = models.IntegerField("节点id", null=False)

    class Meta:
        verbose_name = "接口信息"
        db_table = "API"


class Case(BaseTable):
    """
    用例信息表
    """
    tag = (
        (1, "冒烟测试"),
        (2, "集成测试"),
        (3, "监控脚本"),
    )
    name = models.CharField("用例名称", null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relation = models.IntegerField("节点id", null=False)
    length = models.IntegerField("API个数", null=False)
    tag = models.IntegerField("用例标签", choices=tag, default=2)

    class Meta:
        verbose_name = "用例信息"
        db_table = "Case"


class CaseStep(BaseTable):
    """
    Test Case Step
    """

    name = models.CharField("用例名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=200)
    method = models.CharField("请求方式", null=False, max_length=10)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    step = models.IntegerField("顺序", null=False)

    class Meta:
        verbose_name = "用例信息 Step"
        db_table = "CaseStep"


class HostIP(BaseTable):
    """
    主机配置
    """
    name = models.CharField(null=False, max_length=100)
    value = models.TextField(null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "HOST配置"
        db_table = "HostIP"


class Variables(models.Model):
    """
    全局变量
    """
    key = models.CharField(null=False, max_length=100)
    value = models.CharField(null=False, max_length=1024)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "全局变量"
        db_table = "Variables"


class Report(BaseTable):
    """
    报告存储
    """
    report_type = (
        (1, "调试用例报告"),
        (2, "异步任务报告"),
        (3, "定时任务报告"),
    )

    name = models.CharField("报告名称", null=False, max_length=100)
    type = models.IntegerField("报告类型", choices=report_type, null=False)
    summary = models.TextField("主体信息", null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "测试报告"
        db_table = "Report"


class Relation(models.Model):
    """
    树形结构关系
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tree = models.TextField("结构主题", null=False, default=[])
    type = models.IntegerField("树类型", default=1)

    class Meta:
        verbose_name = "树形结构关系"
        db_table = "Relation"

    # [
    #     {
    #         "name": "testcase",
    #         "body": "body",
    #         "url": "https://www.baidu.com",
    #         "method": "post",
    #         "project": "1",
    #         "relation": 1
    #     }
    # ]
