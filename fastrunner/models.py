from django.db import models

# Create your models here.
from usermanager.models import BaseTable


class Project(BaseTable):
    """
    项目信息表
    """
    name = models.CharField("项目名称", unique=True, null=False, max_length=50)
    desc = models.CharField("简要介绍", max_length=100, null=False)
    responsible = models.CharField("创建人", max_length=20, null=False)

    class Meta:
        verbose_name = "项目信息"
        db_table = "Project"


class Team(BaseTable):
    """
    项目成员
    """

    permission_union = (
        (1, "admin"),
        (2, "read"),
        (3, "write"),
        (4, "delete"),
        (5, "admin")
    )

    account = models.CharField("账号", max_length=20)
    permission = models.IntegerField("权限", choices=permission_union)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "项目成员"
        db_table = "Team"


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

    name = models.CharField("环境名称", null=False, max_length=50)
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

    name = models.CharField("接口名称", null=False, max_length=50)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=100)
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
    name = models.CharField("用例名称", null=False, max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relation = models.IntegerField("节点id", null=False)

    class Meta:
        verbose_name = "用例信息"
        db_table = "Case"


class CaseStep(BaseTable):
    """
    Test Case Step
    """

    name = models.CharField("用例名称", null=False, max_length=50)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=100)
    method = models.CharField("请求方式", null=False, max_length=10)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    step = models.IntegerField("顺序", null=False)

    class Meta:
        verbose_name = "用例信息 Step"
        db_table = "CaseStep"


class DataBase(BaseTable):
    """
    数据库信息表
    """

    db_type = (
        (1, "Sql Server"),
        (2, "MySQL"),
        (3, "Oracle"),
        (4, "Mongodb"),
        (5, "InfluxDB")
    )

    name = models.CharField("数据库名称", null=False, max_length=50)
    server = models.CharField("服务地址", null=False, max_length=100)
    account = models.CharField("登录名", max_length=50, null=False)
    password = models.CharField("登陆密码", max_length=50, null=False)
    type = models.IntegerField('数据库类型', default=2, choices=db_type)
    desc = models.CharField("描述", max_length=50, null=False)

    class Meta:
        verbose_name = "数据库信息"
        db_table = "DataBase"


class FileBinary(models.Model):
    """
    二进制文件流
    """

    name = models.CharField("文件名称", unique=True, null=False, max_length=50)
    body = models.BinaryField("二进制流", null=False)
    size = models.CharField("大小", null=False, max_length=30)

    class Meta:
        verbose_name = "二进制文件"
        db_table = "FileBinary"


class Report(BaseTable):
    """
    报告存储
    """

    name = models.CharField("报告名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    total = models.IntegerField("总共个数", null=False)
    success = models.IntegerField("通过用例")
    failure = models.IntegerField("失败用例")
    skipped = models.IntegerField("跳过用例")
    start_time = models.DateTimeField("开始时间")
    duration = models.CharField("持续时间", max_length=40)

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
