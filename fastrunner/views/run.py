import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes
from fastrunner.utils import loader
from fastrunner import task
from rest_framework.response import Response
from fastrunner.utils.decorator import request_log
from fastrunner.utils.host import parse_host
from fastrunner.utils.parser import Format
from fastrunner import models

"""运行方式
"""
logger = logging.getLogger('FasterRunner')

config_err = {
    "success": False,
    "msg": "指定的配置文件不存在",
    "code": "9999"
}


@api_view(['POST'])
@request_log(level='INFO')
def run_api(request):
    """ run api by body
    """
    name = request.data.pop('config')
    host = request.data.pop("host")
    api = Format(request.data)
    api.parse()

    config = None
    if name != '请选择':
        try:
            config = eval(models.Config.objects.get(name=name, project__id=api.project).body)

        except ObjectDoesNotExist:
            logger.error("指定配置文件不存在:{name}".format(name=name))
            return Response(config_err)

    if host != "请选择":
        host = models.HostIP.objects.get(name=host, project__id=api.project).value.splitlines()
        api.testcase = parse_host(host, api.testcase)

    summary = loader.debug_api(api.testcase, api.project, config=parse_host(host, config))

    return Response(summary)


@api_view(['GET'])
@request_log(level='INFO')
def run_api_pk(request, **kwargs):
    """run api by pk and config
    """
    host = request.query_params["host"]
    api = models.API.objects.get(id=kwargs['pk'])
    name = request.query_params["config"]
    config = None if name == '请选择' else eval(models.Config.objects.get(name=name, project=api.project).body)

    test_case = eval(api.body)
    if host != "请选择":
        host = models.HostIP.objects.get(name=host, project=api.project).value.splitlines()
        test_case = parse_host(host, test_case)

    summary = loader.debug_api(test_case, api.project.id, config=parse_host(host, config))

    return Response(summary)


@api_view(['POST'])
@request_log(level='INFO')
def run_api_tree(request):
    """run api by tree
    {
        project: int
        relation: list
        name: str
        async: bool
        host: str
    }
    """
    # order by id default
    host = request.data["host"]
    project = request.data['project']
    relation = request.data["relation"]
    back_async = request.data["async"]
    name = request.data["name"]
    config = request.data["config"]

    config = None if config == '请选择' else eval(models.Config.objects.get(name=config, project__id=project).body)
    test_case = []

    if host != "请选择":
        host = models.HostIP.objects.get(name=host, project=project).value.splitlines()

    for relation_id in relation:
        api = models.API.objects.filter(project__id=project, relation=relation_id).order_by('id').values('body')
        for content in api:
            api = eval(content['body'])
            test_case.append(parse_host(host, api))

    if back_async:
        task.async_debug_api.delay(test_case, project, name, config=parse_host(host, config))
        summary = loader.TEST_NOT_EXISTS
        summary["msg"] = "接口运行中，请稍后查看报告"
    else:
        summary = loader.debug_api(test_case, project, config=parse_host(host, config))

    return Response(summary)


@api_view(["POST"])
@request_log(level='INFO')
def run_testsuite(request):
    """debug testsuite
    {
        name: str,
        body: dict
        host: str
    }
    """
    body = request.data["body"]
    project = request.data["project"]
    name = request.data["name"]
    host = request.data["host"]

    test_case = []
    config = None

    if host != "请选择":
        host = models.HostIP.objects.get(name=host, project=project).value.splitlines()

    for test in body:
        test = loader.load_test(test, project=project)
        if "base_url" in test["request"].keys():
            config = test
            continue

        test_case.append(parse_host(host, test))

    summary = loader.debug_api(test_case, project, name=name, config=parse_host(host, config))

    return Response(summary)


@api_view(["GET"])
@request_log(level='INFO')
def run_testsuite_pk(request, **kwargs):
    """run testsuite by pk
        {
            project: int,
            name: str,
            host: str
        }
    """
    pk = kwargs["pk"]

    test_list = models.CaseStep.objects. \
        filter(case__id=pk).order_by("step").values("body")

    project = request.query_params["project"]
    name = request.query_params["name"]
    host = request.query_params["host"]

    test_case = []
    config = None

    if host != "请选择":
        host = models.HostIP.objects.get(name=host, project=project).value.splitlines()

    for content in test_list:
        body = eval(content["body"])

        if "base_url" in body["request"].keys():
            config = eval(models.Config.objects.get(name=body["name"], project__id=project).body)
            continue

        test_case.append(parse_host(host, body))

    summary = loader.debug_api(test_case, project, name=name, config=parse_host(host, config))

    return Response(summary)


@api_view(['POST'])
@request_log(level='INFO')
def run_suite_tree(request):
    """run suite by tree
    {
        project: int
        relation: list
        name: str
        async: bool
        host: str
    }
    """
    # order by id default
    project = request.data['project']
    relation = request.data["relation"]
    back_async = request.data["async"]
    report = request.data["name"]
    host = request.data["host"]

    if host != "请选择":
        host = models.HostIP.objects.get(name=host, project=project).value.splitlines()

    test_sets = []
    suite_list = []
    config_list = []
    for relation_id in relation:
        suite = list(models.Case.objects.filter(project__id=project,
                                                relation=relation_id).order_by('id').values('id', 'name'))
        for content in suite:
            test_list = models.CaseStep.objects. \
                filter(case__id=content["id"]).order_by("step").values("body")

            testcase_list = []
            config = None
            for content in test_list:
                body = eval(content["body"])
                if "base_url" in body["request"].keys():
                    config = eval(models.Config.objects.get(name=body["name"], project__id=project).body)
                    continue
                testcase_list.append(parse_host(host, body))
            # [[{scripts}, {scripts}], [{scripts}, {scripts}]]
            config_list.append(parse_host(host, config))
            test_sets.append(testcase_list)
            suite_list = suite_list + suite

    if back_async:
        task.async_debug_suite.delay(test_sets, project, suite_list, report, config_list)
        summary = loader.TEST_NOT_EXISTS
        summary["msg"] = "用例运行中，请稍后查看报告"
    else:
        summary = loader.debug_suite(test_sets, project, suite_list, config_list)

    return Response(summary)


@api_view(["POST"])
@request_log(level='INFO')
def run_test(request):
    """debug single test
    {
        host: str
        body: dict
        project :int
        config: null or dict
    }
    """

    body = request.data["body"]
    config = request.data.get("config", None)
    project = request.data["project"]
    host = request.data["host"]

    if host != "请选择":
        host = models.HostIP.objects.get(name=host, project=project).value.splitlines()

    if config:
        config = eval(models.Config.objects.get(project=project, name=config["name"]).body)

    summary = loader.debug_api(parse_host(host, loader.load_test(body)), project, config=parse_host(host, config))

    return Response(summary)


@api_view(["POST"])
@request_log(level='INFO')
@authentication_classes([])
def automation_test(request):
    """kafka automation test
    {
        "key": 业务线key
        "task_id":"任务id",
        "business_line" : "业务线"
        "ip" : "ip地址",
        "app_name" : "应用名",
        "dev_manager":"开发负责人",   #发布的开发姓名
        "demand_id":"需求ID",
        "version_id":"版本ID",
        "env_flag":"环境标识",
    }
    """

    plan = models.Plan.objects.all()

    for plan_sub in plan:
        if plan_sub.key == request.data["key"] and plan_sub.switch:
            host = None
            if plan_sub.host != "请选择":
                host = models.HostIP.objects.get(name=plan_sub.host, project=plan_sub.project).value.splitlines()

            test_sets = []
            config_list = []

            suite = []

            for index in json.loads(plan_sub.case):
                try:
                    case = models.Case.objects.get(id=index)
                    suite.append({
                        "name": case.name,
                        "id": index
                    })
                except ObjectDoesNotExist:
                    pass

            for content in suite:
                test_list = models.CaseStep.objects. \
                    filter(case__id=content["id"]).order_by("step").values("body")

                testcase_list = []
                config = None
                for content in test_list:
                    body = eval(content["body"])
                    if "base_url" in body["request"].keys():
                        config = eval(models.Config.objects.get(name=body["name"], project=plan_sub.project).body)
                        continue
                    testcase_list.append(parse_host(host, body))

                config_list.append(parse_host(host, config))
                test_sets.append(testcase_list)

            tags = {
                "project": plan_sub.project.id,
                "tag": plan_sub.tag
            }
            task.async_automation_suite.delay(test_sets, tags, suite, request.data, config_list)
            break

    return Response({
        "success": True,
        "msg": "集成自动化用例运行中",
        "code": "0001"
    })
