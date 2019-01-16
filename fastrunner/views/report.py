#! /usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.viewsets import GenericViewSet

from FasterRunner import pagination
from fastrunner import models, serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from fastrunner.utils import response
import json


class ReportView(GenericViewSet):
    """
    报告视图
    """
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = ()
    queryset = models.Report.objects
    serializer_class = serializers.ReportSerializer
    pagination_class = pagination.MyPageNumberPagination

    def list(self, request):
        """报告列表
        """
        project = request.query_params["project"]
        search = request.query_params["search"]
        queryset = self.get_queryset().filter(project__id=project).order_by("-update_time")

        if search != '':
            queryset = queryset.filter(name__contains=search)

        page_report = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page_report, many=True)
        return self.get_paginated_response(serializer.data)

    def delete(self, request, **kwargs):
        """删除报告
        """
        try:
            if kwargs.get('pk'):  # 单个删除
                models.Report.objects.get(id=kwargs['pk']).delete()
            else:
                for content in request.data:
                    models.Report.objects.get(id=content['id']).delete()

        except ObjectDoesNotExist:
            return Response(response.REPORT_NOT_EXISTS)

        return Response(response.REPORT_DEL_SUCCESS)

    def look(self, request, **kwargs):
        """查看报告
        """
        pk = kwargs["pk"]
        summary = models.Report.objects.get(id=pk).summary

        return render_to_response(summary, template_name='report_template.html')

    def download(self, request, **kwargs):
        """下载报告
        """
        pass
