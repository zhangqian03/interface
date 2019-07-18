# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.backends.mysql.base import DatabaseWrapper


# 测试用例表
class TestCases(models.Model):
    system = models.ForeignKey('Systems',on_delete=models.CASCADE,default='')
    case_name = models.CharField(max_length=50, verbose_name='接口名称')
    case_url = models.CharField(max_length=100, verbose_name='接口路径')
    request_method = models.CharField(max_length=10, verbose_name='请求方式')
    request_header = models.CharField(max_length=500, verbose_name='请求头')
    request_body = models.TextField(max_length=65500, verbose_name='请求体')
    checkpoint = models.CharField(max_length=500, verbose_name='校验点')
    case_brief = models.CharField(max_length=500, verbose_name='接口描述')
    case_status = models.BooleanField(default=True, verbose_name='接口状态')
    time = models.DateField(auto_now=True, verbose_name='记录时间')

    class Meta:
        verbose_name = '接口测试案例'
        verbose_name_plural = '接口测试案例'

    def __unicode__(self):
        return self.case_name


# 测试合集表
class CaseBook(models.Model):
    book_name = models.CharField(max_length=50, verbose_name='合集名称')
    book_brief = models.CharField(max_length=500, verbose_name='合集简介')
    run_time = models.DateTimeField(auto_now=False, null=True, verbose_name='执行时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    case_id = models.CharField(max_length=500, verbose_name='用例编号')
    book_status = models.CharField(max_length=10, null=True, verbose_name='测试集合状态')
    case_id_backup = models.CharField(max_length=500, verbose_name='用例编号备份')

    class Meta:
        verbose_name = '接口测试合集'
        verbose_name_plural = '接口测试合集'

    def __unicode__(self):
        return self.book_name


# 测试报告表
class Report(models.Model):
    report_name = models.CharField(max_length=50, verbose_name='报告名称')
    time = models.DateTimeField(auto_now=True, verbose_name='记录时间')
    status = models.CharField(max_length=20, verbose_name='状态')
    case_name = models.CharField(max_length=50, verbose_name='用例名称')

    class Meta:
        verbose_name = '接口测试报告'
        verbose_name_plural = '接口测试报告'

    def __unicode__(self):
        return self.report_name


# 被测系统表
class Systems(models.Model):
    system_id = models.AutoField(max_length=50, verbose_name='系统编号', primary_key=True)
    system_name = models.CharField(max_length=100, verbose_name='系统名称')
    system_desc = models.CharField(max_length=800, verbose_name='系统描述', null=True, blank=True)

    class Meta:
        verbose_name = '被测系统列表'
        verbose_name_plural = '被测系统列表'

    def __unicode__(self):
        return self.system_id


# 测试数据临时表
class TestDataTemp(models.Model):
    book_id = models.CharField(max_length=50, verbose_name='合集编号')
    case_id = models.CharField(max_length=50, verbose_name='用例编号')
    case_data = models.CharField(max_length=1000, null=True, verbose_name='测试数据')

    class Meta:
        verbose_name = '测试数据临时表'
        verbose_name_plural = '测试数据临时表'

    def __unicode__(self):
        return self.book_id


# 用例参数表
class CaseParameter(models.Model):
    book_id = models.CharField(max_length=50, verbose_name='合集编号')
    case_id = models.CharField(max_length=50, verbose_name='用例编号')
    introduce = models.CharField(max_length=50, verbose_name='参数描述')
    input_key = models.CharField(max_length=50, verbose_name='入参key')
    take_method = models.CharField(max_length=50, verbose_name='取值方法')
    input_data = models.CharField(max_length=500, verbose_name='输入数据')
    take_data_sql = models.CharField(max_length=500, verbose_name='取值sql数据')
    take_sql_source = models.CharField(max_length=50, verbose_name='取值sql源')
    take_data_key = models.CharField(max_length=50, verbose_name='取值key数据')
    take_case_id = models.CharField(max_length=50, verbose_name='取值用例编号')

    class Meta:
        verbose_name = '用例参数表'
        verbose_name_plural = '用例参数表'

    def __unicode__(self):
        return self.book_id


# 定时任务表
class Tasks(models.Model):
    book_id = models.CharField(max_length=100, verbose_name='合集ID')
    task_config = models.CharField(max_length=100, null=True, verbose_name='任务配置')
    task_log = models.CharField(max_length=1000, null=True, verbose_name='任务日志')

    class Meta:
        verbose_name = '定时任务表'
        verbose_name_plural = '定时任务表'

    def __unicode__(self):
        return self.book_id


# 附件表
class Attachments(models.Model):
    attachments_name = models.CharField(max_length=100, verbose_name='附件名称')

    class Meta:
        verbose_name = '附件表'
        verbose_name_plural = '附件表'

    def __unicode__(self):
        return self.attachments_name


# 附件关联用例表
class AttachmentsCase(models.Model):
    book_id = models.CharField(max_length=100, verbose_name='合集ID')
    case_id = models.CharField(max_length=100, verbose_name='用例ID')
    send_name = models.CharField(max_length=100, verbose_name='附件发送名称')
    attachments_id = models.CharField(max_length=100, verbose_name='附件ID')

    class Meta:
        verbose_name = '附件关联用例表'
        verbose_name_plural = '附件关联用例表'

    def __unicode__(self):
        return self.book_id
