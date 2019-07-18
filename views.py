# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .Lib import tools
from .apptest.case.authorization import CaseAuth
from .apptest.case.login import CaseLogin
from .apptest.case.register import CaseRegister
from .apptest.case.userbase import CaseUserBase
# from .models import TestCases, TestDataTemp, CaseParameter, Hosts
# from .models import Systems
# from .models import CaseBook
# from .models import Report

from .models import *
import json
import os
import platform
from .api_run import method,run
from django.contrib import auth


# Create your views here.
def main(request):
    return render(request, "main.html")

def index(request):
    return render(request, "login.html")

def home(request):
    return render(request, "home_page.html")

def login_action(request):
    # 处理登录请求
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        verify = auth.authenticate(username=username, password=password)
        if verify is not None:
            auth.login(request, verify)
            response = HttpResponseRedirect('/home/')
            # user_name 用于表示写入浏览器的cookie名
            # username 是用户在浏览器上输入的登录名
            # 3600 是设置cookie信息在浏览器中的保持时间
            # response.set_cookie('cookie_name', username, 3600)
            request.session['cookie_name'] = username  # 将session信息记录在浏览器
            # print(username)
            return response

        else:
            return render(request, 'login.html', {'error': '用户名密码错误.'})

def logout_action(request):
    auth.logout(request)
    return render(request, 'login.html')

@csrf_exempt
def credit_app_operate(request):
    return render(request, "credit_app.html")


@csrf_exempt
def switch_to_config(request):
    return render(request, "config.html")


@csrf_exempt
def switch_hosts(request):
    return render(request, "switch_host.html")

@csrf_exempt
def manage_hosts(request):
    return render(request, "manage_hosts.html")

def switches(request):
    return render(request, "switch_host.html")

@csrf_exempt
def manage_databases(request):
    return render(request, "manage_databases.html")

@csrf_exempt
def config_list(request):
    if request.method == "POST":
        configs_list = method.get_all_config()

        # for i in range(len(configs_list)):
        #     config_dict = {}
        #     config_dict["config_name"] = configs_list[i]
        #     cases_list.append(config_dict)

        query_data = {
            "code": '0',
            "msg": "",
            "data": configs_list
        }

        return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


# @csrf_exempt
# def change_host(request):
#     if request.method == "POST":
#         changed_environment = request.POST.get('host')
#         print(changed_environment)
#         changed_os = request.POST.get('os')
#         hosts = Hosts.objects.filter(id=changed_environment)
#
#         output = open(r'C:\WINDOWS\system32\drivers\etc\HOSTS', 'w')
#
#         for i in hosts:
#             print(eval(i.hosts_content))
#             for x in eval(i.hosts_content):
#                 print(type(x))
#                 output.write(x)
#                 output.write("\n")
#             output.close()
#         ret = {'code': '0',
#                'msg': '更新成功',
#                }
#         return HttpResponse(json.dumps(ret, ensure_ascii=False), charset='utf-8')
#
#     else:
#         ret = {'code': '0',
#                'msg': '系统异常',
#                }
#         return HttpResponse(json.dumps(ret, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def show_host(request):
    output = open(r'C:\WINDOWS\system32\drivers\etc\HOSTS', 'r')

    data = output.readlines()
    data = '<br>'.join(data)
    output.close()
    res = {'code': '0',
           'data': data,
           }
    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def run_script(request):
    if request.is_ajax():
        request_host = request.POST.get('host')
        request_operation = request.POST.get('operation')
        request_username = request.POST.get('username')
        request_password = request.POST.get('password')

        ret = {'code': '1',
               'msg': u'接收成功',
               'data': {'host': request_host,
                        'operation': request_operation,
                        'username': request_username,
                        'password': request_password
                        }
               }
        return HttpResponse(json.dumps(ret, ensure_ascii=False), charset='utf-8')
    else:
        ret = {'code': '2',
               'msg': u'接收失败',
               }
        return HttpResponse(json.dumps(ret))


@csrf_exempt
def register(request):
    if request.method == "POST":
        host = request.POST.get('host')
        phone= request.POST.get('phone')
        password = request.POST.get('password')
        idcard=request.POST.get('idcard')
        name = request.POST.get('name')
        reg = CaseRegister('register')
        res =reg.register(host=str(host),phone=str(phone),password=str(password),
                          idcard=str(idcard),name=name)
        return HttpResponse(res)
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        env = request.POST.get("environment")
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        cs = CaseLogin('testlogin')
        res = cs.testlogin(host=env, username=usr, password=pwd)
        return HttpResponse(res)
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def userinfo(request):
    if request.method == 'POST':
        env = request.POST.get("environment")
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        cs = CaseLogin('testlogin')
        cs.testlogin(host=env,username=usr,password=pwd)

        ub = CaseUserBase('testuserbase')
        res = ub.testuserbase(host=env)

        return HttpResponse(res)
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def occupation(request):
    if request.method == 'POST':
        env = request.POST.get("environment")
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        cs = CaseLogin('testlogin')
        cs.testlogin(host=env,username=usr,password=pwd)

        ub = CaseUserBase('testoccupation')
        res = ub.testoccupation(host=env)

        return HttpResponse("success {}".format(res))

    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def userrelation(request):
    if request.method == 'POST':
        env = request.POST.get("environment")
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        cs = CaseLogin('testlogin')
        cs.testlogin(host=env,username=usr,password=pwd)

        ub = CaseUserBase('testuserrelation')
        res = ub.testuserrelation(host=env)

        return HttpResponse(res)

    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def operatorion(request):
    if request.method == 'POST':
        env,usr,pwd = request.POST.get("environment"),request.POST.get('username'),request.POST.get('password')
        cs = CaseLogin('testlogin')
        cs.testlogin(host=env,username=usr,password=pwd)
        au = CaseAuth('testAuthorization')
        res = au.testAuthorization(host=env)

        return HttpResponse(res)

    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def peoplesbank(request):
    if request.method == 'POST':
        env,usr,pwd = request.POST.get("environment"),request.POST.get('username'),request.POST.get('password')
        name,idcard= request.POST.get('name'),request.POST.get('idcard')


        cs = CaseLogin('testlogin')
        cs.testlogin(host=env, username=usr, password=pwd)

        au = CaseAuth('PeoplesBank')
        res = au.PeoplesBank(host=env,idcard=idcard,name=name)
        return HttpResponse(res)
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def pbc_modify(request):
    if request.method == 'POST':
        test_environment = request.POST.get('environment')
        test_user = request.POST.get('user')
        test_password = request.POST.get('password')

        req_list = [test_environment, test_user, test_password]

        tools.hosts_modify(test_environment)  # 根据post参数environment修改执行机hosts

        ret = {'errorCode': '0',
               'msg': '执行成功',
               'parameters': req_list
               }
        return HttpResponse(json.dumps(ret), content_type="application/json")

    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def carrier_modify(request):
    if request.method == 'POST':
        test_environment = request.POST.get('environment')
        test_user = request.POST.get('user')
        test_password = request.POST.get('password')

        req_list = [test_environment, test_user, test_password]

        ret = {'errorCode': '0',
               'msg': '执行成功',
               'parameters': req_list
               }

        return HttpResponse(json.dumps(ret), content_type="application/json")
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def taobao_modify(request):
    if request.method == 'POST':
        test_environment = request.POST.get('environment')
        test_user = request.POST.get('user')
        test_password = request.POST.get('password')

        req_list = [test_environment, test_user, test_password]

        ret = {'errorCode': '0',
               'msg': '执行成功',
               'parameters': req_list
               }

        return HttpResponse(json.dumps(ret), content_type="application/json")
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def AliPay_modify(request):
    if request.method == 'POST':
        test_environment = request.POST.get('environment')
        test_user = request.POST.get('user')
        test_password = request.POST.get('password')

        req_list = [test_environment, test_user, test_password]

        ret = {'errorCode': '0',
               'msg': '执行成功',
               'parameters': req_list
               }

        return HttpResponse(json.dumps(ret), content_type="application/json")
    else:
        return HttpResponse('请求异常,执行失败')

@csrf_exempt
def get_all_gui(request):
    return render(request, "credit_app_all.html")

@csrf_exempt
def get_all_cases(request):
    cases = TestCases.objects.all()
    cases_count = TestCases.objects.count()
    cases_list = []
    for i in cases:
        cases_dict = {}
        cases_dict["id"] = str(i.id)
        cases_dict["system"] = str(i.system)
        cases_dict["name"] = str(i.case_name)
        cases_dict["url"] = str(i.case_url)
        cases_dict["method"] = str(i.request_method)
        cases_dict["header"] = str(i.request_header)
        cases_dict["body"] = str(i.request_body)
        cases_dict["checkpoint"] = str(i.checkpoint)
        cases_dict["brief"] = str(i.case_brief)
        cases_dict["status"] = str(i.case_status)
        cases_dict["time"] = str(i.time)
        cases_list.append(cases_dict)

    # print(cases_list)
    all_data = {
          "code": 0,
          "msg": "",
          "count": cases_count,
          "data": cases_list}

    return HttpResponse(json.dumps(all_data, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def add_test_case(request):
    if request.method == 'POST':
        system = request.POST.get('system')
        case_name = request.POST.get('caseName')
        brief = request.POST.get('brief')
        method = request.POST.get('method')
        url = request.POST.get('testUrl')
        header = request.POST.get('header')
        body = request.POST.get('body')
        checkpoint = request.POST.get('checkPoint')

        TestCases.objects.create(system_id=system,case_name=case_name,case_brief=brief,
                                 case_url=url,request_method=method,request_header=header,
                                 request_body=body,checkpoint=checkpoint)
        res = {
            "code": 0,
            "msg": "数据新增成功"
        }

        # print(type(json.dumps(res)))
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')

#  添加测试合集
@csrf_exempt
def add_case_book(request):
    if request.method == 'POST':
        book_name = request.POST.get('bookName')
        book_brief = request.POST.get('bookBrief')
        CaseBook.objects.create(book_name=book_name, book_brief=book_brief)
        res = {
            "code": '0',
            "msg": "数据新增成功"
        }

        print(type(json.dumps(res)))
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


#  测试合集名称描述编辑保存
@csrf_exempt
def book_save(request):
    book_id = request.POST.get('bookId')
    book_name = request.POST.get('bookName')
    book_brief = request.POST.get('bookBrief')
    case_id = request.POST.get('caseId')
    backup = CaseBook.objects.filter(id=book_id)[0].case_id_backup
    try:
        eval(case_id)
    except BaseException as e:
        query_data = {
            "code": '0',
            "msg": "输入数据格式错误，{}".format(e),
        }
        return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
    print(set(eval(case_id)), eval(case_id))
    if len(eval(case_id)) != len(set(eval(case_id))):
        query_data = {
            "code": '0',
            "msg": "数据重复，请重新输入",
        }
        return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
    elif len(eval(case_id)) > len(eval(backup)):
        query_data = {
            "code": '0',
            "msg": "不可新增其他数据，请重新输入",
        }
        return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
    elif len(eval(case_id)) < len(eval(backup)):
        status = ''
        for i in range(len(eval(case_id))):
            if eval(case_id)[i] not in eval(backup):
                status = '1'
        if status == '1':
            query_data = {
                "code": '0',
                "msg": "不可新增其他数据，请重新输入",
            }
            return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
        else:
            CaseBook.objects.filter(id=book_id).update(book_name=book_name, book_brief=book_brief, case_id=case_id)
            query_data = {
                "code": '0',
                "msg": "保存成功",
            }
            return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')

    elif len(eval(case_id)) == len(eval(backup)):
        status = ''
        for i in range(len(eval(case_id))):
            if eval(case_id)[i] not in eval(backup):
                status = '1'
        if status == '1':
            query_data = {
                "code": '0',
                "msg": "不可新增其他数据，请重新输入",
            }
            return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
        else:
            if len(case_id) == len(backup):
                CaseBook.objects.filter(id=book_id).update(book_name=book_name, book_brief=book_brief, case_id=case_id
                                                           , case_id_backup=case_id)
                query_data = {
                    "code": '0',
                    "msg": "排序更新成功",
                }
                return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
            else:
                query_data = {
                    "code": '0',
                    "msg": "请查看是否缺少逗号",
                }
                return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


# 测试合集复制
@csrf_exempt
def book_copy(request):
    book_id = request.POST.get('bookId')
    case_id = CaseBook.objects.filter(id=book_id)[0].case_id
    case_id_backup = CaseBook.objects.filter(id=book_id)[0].case_id_backup
    try:
        CaseBook.objects.create(case_id=case_id, case_id_backup=case_id_backup)
    except BaseException as e:
        print("新增合集失败，{}".format(e))
        query_data = {
            "code": '0',
            "msg": "新增合集失败，{}".format(e),
        }
        return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
    else:
        new_book_id = CaseBook.objects.all().order_by('-id')[0].id
        if case_id != '':
            for x in range(len(eval(case_id))):
                TestDataTemp.objects.create(book_id=new_book_id, case_id=eval(case_id)[x])
        files = AttachmentsCase.objects.filter(book_id=book_id)
        for i in files:
            AttachmentsCase.objects.create(book_id=new_book_id, case_id=i.case_id, send_name=i.send_name
                                           , attachments_id=i.attachments_id)
        params = CaseParameter.objects.filter(book_id=book_id)
        for p in params:
            CaseParameter.objects.create(book_id=new_book_id, case_id=p.case_id, introduce=p.introduce
                                         , input_key=p.input_key, input_data=p.input_data, take_method=p.take_method
                                         , take_data_sql=p.take_data_sql, take_sql_source=p.take_sql_source
                                         , take_data_key=p.take_data_key, take_case_id=p.take_case_id)
        query_data = {
             "code": '0',
             "msg": "复制新增成功",
        }
        return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


#  添加测试合集用例
@csrf_exempt
def add_book_case(request):
    if request.method == 'POST':
        case_id = request.POST.get('caseId')
        book_id = request.POST.get('bookId')
        data = list(CaseBook.objects.filter(id=book_id).values('case_id'))
        backup = CaseBook.objects.filter(id=book_id)[0].case_id_backup
        if len(data[0]['case_id']) == len(backup):
            if data[0]['case_id'] == '':  # 如果用例id集合为空，直接赋值
                TestDataTemp.objects.create(book_id=book_id, case_id=str(case_id)).save()
                case_id = str(case_id) + ','
                CaseBook.objects.filter(id=book_id).update(case_id=case_id)
                CaseBook.objects.filter(id=book_id).update(case_id_backup=case_id)

                res = {
                    "code": '0',
                    "msg": "添加用例成功"
                }
                return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
            else:
                state = str()                                   # 用例id如存在用例id集合中，给出提示
                for x in range(len(eval(data[0]['case_id']))):
                    if int(case_id) == eval(data[0]['case_id'])[x]:
                        state = '1'
                        break

                if state == '1':
                    res = {
                        "code": '0',
                        "msg": "用例已存在"
                    }
                    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
                else:
                    TestDataTemp.objects.create(book_id=book_id, case_id=case_id)
                    cases_id = data[0]['case_id'] + case_id + ','  # 累计添加用例id
                    CaseBook.objects.filter(id=book_id).update(case_id=cases_id)
                    CaseBook.objects.filter(id=book_id).update(case_id_backup=cases_id)
                    res = {
                        "code": '0',
                        "msg": "添加用例成功"
                    }
                    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
        else:
            res = {
                "code": '0',
                "msg": "请先还原用例编号再添加用例"
            }
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        res = {
            "code": '0',
            "msg": "请求异常,执行失败"
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def delete_case_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('bookId')
        TestDataTemp.objects.filter(book_id=book_id).delete()
        CaseParameter.objects.filter(book_id=book_id).delete()
        CaseBook.objects.filter(id=book_id).delete()
        AttachmentsCase.objects.filter(book_id=book_id).delete()

        res = {
            "code": '0',
            "msg": "数据删除成功"
        }

        # print(type(json.dumps(res)))
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def delete_book_case(request):
    if request.method == 'POST':
        book_id = request.POST.get('bookId')
        case_id = request.POST.get('caseId')
        cases_id = list(CaseBook.objects.filter(id=book_id).values('case_id'))
        backup = CaseBook.objects.filter(id=book_id)[0].case_id_backup
        if len(cases_id[0]['case_id']) == len(backup):
            if len(eval(cases_id[0]['case_id'])) == 1:
                param_id = list(CaseParameter.objects.filter(book_id=book_id).values('take_case_id'))
                status = str()
                for x in range(len(param_id)):
                    if param_id[x]['take_case_id'] == case_id:
                        res = {
                            "code": '0',
                            "msg": "用例被其他参数引用，不能删除"
                        }
                        status = '1'
                        break
                if status != '1':
                    CaseBook.objects.filter(id=book_id).update(case_id='')
                    CaseBook.objects.filter(id=book_id).update(case_id_backup='')
                    TestDataTemp.objects.filter(book_id=book_id).filter(case_id=case_id).delete()
                    CaseParameter.objects.filter(book_id=book_id).filter(case_id=case_id).delete()
                    AttachmentsCase.objects.filter(book_id=book_id, case_id=case_id).delete()
                    res = {
                        "code": '0',
                        "msg": "数据删除成功"
                    }
            else:
                cases_id = list(eval(cases_id[0]['case_id']))
                param_id = list(CaseParameter.objects.filter(book_id=book_id).values('take_case_id'))
                status = str()
                for i in range(len(param_id)):
                    if param_id[i]['take_case_id'] == case_id:
                        res = {
                            "code": '0',
                            "msg": "用例被其他参数引用，不能删除"
                        }
                        status = '1'
                        break
                if status != '1':
                    for x in range(len(cases_id)):
                        if int(case_id) == cases_id[x]:
                            del cases_id[x]
                            break
                    cases_id = ','.join(str(s) for s in cases_id if s not in ['NONE', 'NULL']) + ','
                    CaseBook.objects.filter(id=book_id).update(case_id=cases_id)
                    CaseBook.objects.filter(id=book_id).update(case_id_backup=cases_id)
                    TestDataTemp.objects.filter(book_id=book_id).filter(case_id=case_id).delete()
                    CaseParameter.objects.filter(book_id=book_id).filter(case_id=case_id).delete()
                    AttachmentsCase.objects.filter(book_id=book_id, case_id=case_id).delete()

                    res = {
                        "code": '0',
                        "msg": "数据删除成功"
                    }
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
        else:
            res = {
                "code": '0',
                "msg": "请先还原用例编号再添加用例"
            }
            # print(type(json.dumps(res)))
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def delete_case_param(request):
    if request.method == 'POST':
        case_param = request.POST.get('case_param')
        CaseParameter.objects.filter(id=case_param).delete()
        res = {
            "code": '0',
            "msg": "数据删除成功"
        }

        # print(type(json.dumps(res)))
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def delete_test_case(request):
    if request.method == 'POST':
        case_id = request.POST.get('caseId')
        TestCases.objects.filter(id=case_id).delete()

        res = {
            "code": '0',
            "msg": "数据删除成功"
        }

        # print(type(json.dumps(res)))
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')

@csrf_exempt
def update_test_case(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        system = request.POST.get('system')
        case_name = request.POST.get('caseName')
        brief = request.POST.get('brief')
        method = request.POST.get('method')
        url = request.POST.get('testUrl')
        header = request.POST.get('header')
        body = request.POST.get('body')
        checkpoint = request.POST.get('checkPoint')

        try:
            the_case = TestCases.objects.filter(id=id)
            # print(the_case[0].system.system_name)
            # print(the_case[0].case_name)
            # print(the_case[0].case_brief)
            the_case.update(case_name=case_name,case_brief=brief,request_method=method,
                            case_url=url,request_header=header,request_body=body,checkpoint=checkpoint)
            the_case.save()

        except TestCases.DoesNotExist:
            res = {
                "code": 1,
                "msg": "请求数据不存在"
            }
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')

        finally:
            res = {
                "code": 0,
                "msg": "数据更新成功"
            }
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def copy_test_case(request):
    if request.method == 'POST':
        system = request.POST.get('system')
        method = request.POST.get('method')
        url = request.POST.get('url')
        body = request.POST.get('body')

        TestCases.objects.create(system_id=system,case_name='',case_brief='',
                                 case_url=url,request_method=method,request_header='',
                                 request_body=body,checkpoint='')
        res = {
            "code": '0',
            "msg": "复制新增成功"
        }

        # print(type(json.dumps(res)))
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def query_test_case(request):
    system = request.GET.get('query_system')
    condition = request.GET.get('query_condition')
    content = request.GET.get('query_content')
    # 获取当前请求页码
    page = request.GET.get('page')
    # 获取前端 tabel.render下的limit
    row = request.GET.get('limit')
    # 计算单次返回的列表区间
    i = (int(page) - 1) * int(row)
    j = (int(page) - 1) * int(row) + int(row)
    # print(i,j)

    if condition == "用例说明":
        print('按照用例说明查询.')
        cases = TestCases.objects.filter(case_brief__contains=content, system__system_id=system)
    elif condition == "用例名称":
        print('按照用例名称查询.')
        cases = TestCases.objects.filter(case_name__contains=content, system__system_id=system)
    elif condition == "请求地址":
        print('按照请求地址查询.')
        cases = TestCases.objects.filter(case_url__contains=content, system__system_id=system)
    elif condition == "请求方式":
        print('按照请求方式查询.')
        cases = TestCases.objects.filter(request_method__contains=content, system__system_id=system)
    elif condition == "所属系统":
        print('按照所属系统查询.')
        cases = TestCases.objects.filter(system__system_id=content)
    else:
        print('查询全部数据.')
        cases = TestCases.objects.all()

    total = cases.count()
    cases = cases[i:j]
    resultdict ={}
    resultdict['total'] = total

    cases_list = []
    for i in cases:
        cases_dict = {}
        cases_dict["id"] = str(i.id)
        cases_dict["system"] = str(i.system.system_id)
        cases_dict["name"] = str(i.case_name)
        cases_dict["url"] = str(i.case_url)
        cases_dict["method"] = str(i.request_method)
        cases_dict["header"] = str(i.request_header)
        cases_dict["body"] = str(i.request_body)
        cases_dict["checkpoint"] = str(i.checkpoint)
        cases_dict["brief"] = str(i.case_brief)
        if i.case_status == 1:
            cases_dict["status"] = '<span style="color:#32CD32">' + '成功' + '</span>'
        else:
            cases_dict["status"] = '<span style="color:#FF6347">' + '失败' + '</span>'
        # cases_dict["status"] = '<span style="color:#32CD32">' + str(i.case_status) + '</span>'
        cases_dict["time"] = str(i.time)
        cases_list.append(cases_dict)

    print("记录个数共: %s" %total)
    print("记录为: %s" %cases_list)

    query_data = {
        "code": 0,
        "msg": "数据查询成功",
        "count": total,
        "data": cases_list}

    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def loading_system_list(request):
    systems = Systems.objects.all()
    system_count = Systems.objects.count()
    system_list = []
    for i in systems:
        system_list.append(i.system_name)

    print("系统列表: %s" %system_list)

    all_data = {
          "code": 0,
          "msg": "",
          "count": system_count,
          "data": system_list}

    return JsonResponse(all_data,safe=False)

@csrf_exempt
def loading_system_case_list(request):
    systems = Systems.objects.all()
    system_count = Systems.objects.count()

    name = []
    id = []
    for i in systems:
        name.append(i.system_name)
        id.append(i.system_id)

    print("系统列表: %s" %id)

    all_data = {
          "code": '0',
          "msg": "",
          "count": system_count,
          "name": name,
          "id": id
    }
    print(all_data)
    return JsonResponse(all_data, safe=False)

@csrf_exempt
def loading_book_case_list(request):
    book_id = request.POST.get('book_id')
    print(book_id)
    cases_id = list(CaseBook.objects.filter(id=book_id).values('case_id'))
    if len(cases_id[0]['case_id']) == 1:
        case = TestCases.objects.filter(id=cases_id)
    else:
        cases_id = eval(cases_id[0]['case_id'])
        case = TestCases.objects.filter(id__in=cases_id)
    cases_list = []
    for i in case:
        cases_dict = {}
        cases_dict["case_id"] = str(i.id)
        cases_dict["case_name"] = str(i.case_name)
        cases_list.append(cases_dict)

    data = {
          "code": 0,
          "msg": "",
          "data": cases_list
    }

    return JsonResponse(data, safe=False)


@csrf_exempt
def query_case_book(request):
    content = request.GET.get('query_content')
    # 获取当前请求页码
    page = request.GET.get('page')
    # 获取前端 tabel.render下的limit
    row = request.GET.get('limit')
    # 计算单次返回的列表区间
    i = (int(page) - 1) * int(row)
    j = (int(page) - 1) * int(row) + int(row)
    # print(i,j)

    if content != "":
        print('按照合集名称查询.')
        book = CaseBook.objects.filter(book_name__contains=content)
    else:
        print('查询全部数据.')
        book = CaseBook.objects.all()

    total = book.count()
    books = book[i:j]
    resultdict ={}
    resultdict['total'] = total

    books_list = []
    for i in books:
        books_dict = {}
        books_dict["bookId"] = str(i.id)
        books_dict["bookName"] = str(i.book_name)
        books_dict["bookBrief"] = str(i.book_brief)
        books_dict["caseId"] = str(i.case_id)
        books_dict["caseIdBackup"] = str(i.case_id_backup)
        if i.book_status is None:
            books_dict["book_status"] = '<span style="color:#FF6347">' + '未执行' + '</span>'
        elif i.book_status == '0':
            books_dict["book_status"] = '<span style="color:#32CD32">' + '成功' + '</span>'
        elif i.book_status == '1':
            books_dict["book_status"] = '<span style="color:#FF6347">' + '失败' + '</span>'
        elif i.book_status == '2':
            books_dict["book_status"] = '<span style="color:#FF6347">' + '异常' + '</span>'
        elif i.book_status == '3':
            books_dict["book_status"] = '<span style="color:#FF6347">' + '执行中' + '</span>'
        books_dict["runTime"] = str(i.run_time)
        books_dict["updateTime"] = str(i.update_time)
        books_list.append(books_dict)

    print("记录个数共: %s" %total)
    print("记录为: %s" %books_list)

    query_data = {
        "code": 0,
        "msg": "数据查询成功",
        "count": total,
        "data": books_list}

    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def query_book_case(request):
    book_id = request.GET.get('book_id')
    # 获取当前请求页码
    page = request.GET.get('page')
    # 获取前端 tabel.render下的limit
    row = request.GET.get('limit')
    # 计算单次返回的列表区间
    i = (int(page) - 1) * int(row)
    j = (int(page) - 1) * int(row) + int(row)
    # print(i,j)
    cases_id = list(CaseBook.objects.filter(id=book_id).values('case_id'))
    if cases_id[0]['case_id'] == '':
        query_data = {
            "code": 0,
            "msg": "数据查询成功",
            "count": 0,
            "data": ''}
    else:
        cases_id = eval(cases_id[0]['case_id'])
        print(cases_id)
        case = []
        if type(cases_id) == tuple:
            for x in range(len(cases_id)):
                cases = list(TestCases.objects.filter(id=cases_id[x]))
                case = case + cases
            cases = case
        else:
            cases = TestCases.objects.filter(id=cases_id)
        total = len(cases)
        cases = cases[i:j]
        resultdict = {}
        resultdict['total'] = total
        cases_list = []
        for i in cases:
            cases_dict = {}
            cases_dict["id"] = str(i.id)
            cases_dict["system"] = str(i.system)
            cases_dict["name"] = str(i.case_name)
            cases_dict["url"] = str(i.case_url)
            cases_dict["method"] = str(i.request_method)
            cases_dict["header"] = str(i.request_header)
            cases_dict["body"] = str(i.request_body)
            cases_dict["checkpoint"] = str(i.checkpoint)
            cases_dict["brief"] = str(i.case_brief)
            # if i.case_status == 1:
            #     cases_dict["status"] = '<span style="color:#32CD32">' + str(i.case_status) + '</span>'
            # else:
            #     cases_dict["status"] = '<span style="color:#FF6347">' + str(i.case_status) + '</span>'
            # cases_dict["status"] = '<span style="color:#32CD32">' + str(i.case_status) + '</span>'
            cases_dict["time"] = str(i.time)
            cases_list.append(cases_dict)

        print("记录个数共: %s" % total)
        print("记录为: %s" % cases_list)

        query_data = {
            "code": 0,
            "msg": "数据查询成功",
            "count": total,
            "data": cases_list}

    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def query_case_param(request):
    book_id = request.GET.get('book_id')
    case_id = request.GET.get('case_id')
    print(book_id,case_id)
    # 获取当前请求页码
    page = request.GET.get('page')
    # 获取前端 tabel.render下的limit
    row = request.GET.get('limit')
    # 计算单次返回的列表区间
    i = (int(page) - 1) * int(row)
    j = (int(page) - 1) * int(row) + int(row)
    # print(i,j)
    if case_id is None:
        param = CaseParameter.objects.filter(book_id=book_id)
    else:
        param = CaseParameter.objects.filter(book_id=book_id).filter(case_id=case_id)

    total = param.count()
    params = param[i:j]
    resultdict ={}
    resultdict['total'] = total

    params_list = []
    for i in params:
        params_dict = {}
        params_dict["param_id"] = str(i.id)
        params_dict["book_id"] = str(i.book_id)
        params_dict["case_id"] = str(i.case_id)
        case_name = TestCases.objects.filter(id=i.case_id).values('case_name')
        case_name = case_name[0]['case_name']
        params_dict["case_name"] = case_name
        params_dict["introduce"] = str(i.introduce)
        params_dict["input_key"] = str(i.input_key)
        params_dict["take_method"] = str(i.take_method)
        params_dict["input_data"] = str(i.input_data)
        params_dict["sql_source"] = str(i.take_sql_source)
        params_dict["take_data_sql"] = str(i.take_data_sql)
        if i.take_case_id == '':
            take_case_name = ''
        else:
            take_case_name = TestCases.objects.filter(id=i.take_case_id).values('case_name')
            take_case_name = take_case_name[0]['case_name']
        params_dict["take_case_id"] = str(i.take_case_id)
        params_dict["take_case_name"] = take_case_name
        params_dict["take_data_key"] = str(i.take_data_key)
        params_list.append(params_dict)

    print("记录个数共: %s" % total)
    print("记录为: %s" % params_list)

    query_data = {
        "code": 0,
        "msg": "数据查询成功",
        "count": total,
        "data": params_list}

    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def save_param(request):
    book_id = request.POST.get('book_id')
    case_id = request.POST.get('case_id')
    introduce = request.POST.get('introduce')
    input_key = request.POST.get('input_key')
    take_method = request.POST.get('take_method')
    input_data = request.POST.get('input_data')
    take_data_sql = request.POST.get('take_data_sql')
    take_case_id = request.POST.get('case')
    take_data_key = request.POST.get('take_data_key')
    sql_source = request.POST.get('sql_source')
    repeat = ''
    param = CaseParameter.objects.filter(book_id=book_id, case_id=case_id)
    param_b = CaseParameter.objects.filter(book_id=book_id)
    for x in param:
        if input_key == x.input_key:
            repeat = '1'
            break
    for i in param_b:
        if introduce == i.introduce:
            repeat = '2'
            break
    if repeat == '1':
        query_data = {
            "code": '1',
            "msg": "保存失败，同一个用例中入参键值不能重复",
        }
    elif repeat == '2':
        query_data = {
            "code": '1',
            "msg": "保存失败，同一个合集中参数名称不能重复",
        }
    else:
        if take_method == 'SQL':
            if take_data_sql == '' or sql_source == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，取值SQL或SQL源不能为空",
                }
            else:
                CaseParameter.objects.create(book_id=book_id,
                                             case_id=case_id,
                                             introduce=introduce,
                                             input_key=input_key,
                                             take_method=take_method,
                                             take_sql_source=sql_source,
                                             take_data_sql=take_data_sql)
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
        elif take_method == 'JSON':
            if take_case_id == '' or take_data_key == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，取值用例或取值键值不能为空",
                }
            else:
                CaseParameter.objects.create(book_id=book_id,
                                             case_id=case_id,
                                             introduce=introduce,
                                             input_key=input_key,
                                             take_method=take_method,
                                             take_case_id=take_case_id,
                                             take_data_key=take_data_key)
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
        elif take_method == 'INPUT':
            if input_data == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，输入数据为空",
                }
            else:
                CaseParameter.objects.create(book_id=book_id,
                                             case_id=case_id,
                                             introduce=introduce,
                                             input_key=input_key,
                                             take_method=take_method,
                                             input_data=input_data
                                             )
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
        elif take_method == 'CHOOSE INPUT':
            if take_case_id == '' or take_data_key == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，取值用例和取值键值不能为空",
                }
            else:
                # param = CaseParameter.objects.filter(book_id=book_id, case_id=take_case_id, input_key=take_data_key)
                # way = ''
                # for i in param:
                #     way = i.take_method
                # if way != 'INPUT':
                #     query_data = {
                #         "code": '1',
                #         "msg": "保存失败，CHOOSE INPUT取值对应参数方法应该为INPUT",
                #     }
                # else:
                CaseParameter.objects.create(book_id=book_id,
                                             case_id=case_id,
                                             introduce=introduce,
                                             input_key=input_key,
                                             take_method=take_method,
                                             take_case_id=take_case_id,
                                             take_data_key=take_data_key)
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
        elif take_method == 'SPLIT DATA':
            if input_data == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，输入数据为空",
                }
            else:
                CaseParameter.objects.create(book_id=book_id,
                                             case_id=case_id,
                                             introduce=introduce,
                                             input_key=input_key,
                                             take_method=take_method,
                                             input_data=input_data
                                             )
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def update_param(request):
    param_id = request.POST.get('param_id')
    book_id = request.POST.get('book_id')
    case_id = request.POST.get('case_id')
    introduce = request.POST.get('introduce')
    input_key = request.POST.get('input_key')
    take_method = request.POST.get('take_method')
    input_data = request.POST.get('input_data')
    take_data_sql = request.POST.get('take_data_sql')
    take_case_id = request.POST.get('case')
    take_data_key = request.POST.get('take_data_key')
    sql_source = request.POST.get('sql_source')

    repeat = ''
    param = CaseParameter.objects.filter(book_id=book_id, case_id=case_id).exclude(id=param_id)
    param_b = CaseParameter.objects.filter(book_id=book_id).exclude(id=param_id)
    for x in param:
        if input_key == x.input_key:
            repeat = '1'
            break
    for i in param_b:
        if introduce == i.introduce:
            repeat = '2'
            break
    if repeat == '1':
        query_data = {
            "code": '1',
            "msg": "保存失败，同一个用例中入参键值不能重复",
        }
    elif repeat == '2':
        query_data = {
            "code": '1',
            "msg": "保存失败，同一个合集中参数名称不能重复",
        }
    else:
        if take_method == 'SQL':
            if take_data_sql == '' or sql_source == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，取值SQL或SQL源不能为空",
                }
            else:
                CaseParameter.objects.filter(id=param_id).update(introduce=introduce,
                                                                 input_key=input_key,
                                                                 take_method=take_method,
                                                                 input_data='',
                                                                 take_sql_source=sql_source,
                                                                 take_data_sql=take_data_sql,
                                                                 take_case_id='',
                                                                 take_data_key=''
                                                                 )
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
        elif take_method == 'JSON':
            if take_case_id == '' or take_data_key == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，取值用例和取值键值不能为空",
                }
            else:
                CaseParameter.objects.filter(id=param_id).update(introduce=introduce,
                                                                 input_key=input_key,
                                                                 take_method=take_method,
                                                                 input_data='',
                                                                 take_sql_source='',
                                                                 take_data_sql='',
                                                                 take_case_id=take_case_id,
                                                                 take_data_key=take_data_key
                                                                 )
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
        elif take_method == 'INPUT':
            if input_data == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，输入数据为空",
                }
            else:
                CaseParameter.objects.filter(id=param_id).update(introduce=introduce,
                                                                 input_key=input_key,
                                                                 take_method=take_method,
                                                                 input_data=input_data,
                                                                 take_sql_source='',
                                                                 take_data_sql='',
                                                                 take_case_id='',
                                                                 take_data_key=''
                                                                 )
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
        elif take_method == 'CHOOSE INPUT':
            if take_case_id == '' or take_data_key == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，取值用例和取值键值不能为空",
                }
            else:
                # param = CaseParameter.objects.filter(book_id=book_id, case_id=take_case_id, input_key=take_data_key)
                # way = ''
                # for i in param:
                #     way = i.take_method
                # if way != 'INPUT':
                #     query_data = {
                #         "code": '1',
                #         "msg": "保存失败，CHOOSE INPUT取值对应参数方法应该为INPUT",
                #     }
                # else:
                CaseParameter.objects.filter(id=param_id).update(introduce=introduce,
                                                                 input_key=input_key,
                                                                 take_method=take_method,
                                                                 input_data='',
                                                                 take_sql_source='',
                                                                 take_data_sql='',
                                                                 take_case_id=take_case_id,
                                                                 take_data_key=take_data_key)
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
        elif take_method == 'SPLIT DATA':
            if input_data == '':
                query_data = {
                    "code": '1',
                    "msg": "保存失败，输入数据为空",
                }
            else:
                CaseParameter.objects.filter(id=param_id).update(introduce=introduce,
                                                                 input_key=input_key,
                                                                 take_method=take_method,
                                                                 input_data=input_data,
                                                                 take_sql_source='',
                                                                 take_data_sql='',
                                                                 take_case_id='',
                                                                 take_data_key=''
                                                                 )
                query_data = {
                    "code": '0',
                    "msg": "保存成功",
                }
    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def save_list_param(request):
    param_id = request.POST.get('param_id')
    input_data = request.POST.get('input_data')
    take_data_sql = request.POST.get('take_data_sql')
    take_method = request.POST.get('take_method')
    print(param_id, input_data, take_method, take_data_sql)
    if take_method == 'INPUT':
        CaseParameter.objects.filter(id=param_id).update(input_data=input_data)
        query_data = {
            "code": '0',
            "msg": "保存成功",
        }
    elif take_method == 'SQL':
        CaseParameter.objects.filter(id=param_id).update(take_data_sql=take_data_sql)
        query_data = {
            "code": '0',
            "msg": "保存成功",
        }
    else:
        query_data = {
            "code": '1',
            "msg": "请选择INPUT或SQL类型保存",
        }

    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def get_executor(request):
    return render(request, "executor.html")


@csrf_exempt
def case_book(request):
    return render(request, "case_book.html")

@csrf_exempt
def book_list(request):
    return render(request, "book_list.html")

@csrf_exempt
def book_task(request):
    return render(request, "book_task.html")

@csrf_exempt
def case_book_manage(request):
    return render(request, "case_book_management.html")

@csrf_exempt
def run_test_case(request):
    if request.method == 'POST':
        case_id = request.POST.get('caseId')
        case = run.TestOperate()  # 实例化unittest对象
        test_result = case.test_report(case_id)
        print(test_result)
        print(test_result.result)
        TestCases.objects.filter(id=case_id).update(time=method.get_now_date())
        flag = test_result.result[0][0]
        if flag == 0:
            TestCases.objects.filter(id=case_id).update(case_status=1)
        else:
            TestCases.objects.filter(id=case_id).update(case_status=0)
        # 返回状态为0或者1时,回调报文会有message信息

        if test_result.result[0][0] == 0:
            res = {
                "code": test_result.result[0][0],
                "msg": '成功'
            }
        elif test_result.result[0][0] == 1:
            res = {
                "code": test_result.result[0][0],
                "msg": '失败'
            }
        elif test_result.result[0][0] == 2:
            res = {
                "code": test_result.result[0][0],
                "msg": '系统异常'
            }
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        res = {
            "code": '2',
            "msg": '系统异常'
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def run_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('bookId')
        case_id = list(CaseBook.objects.filter(id=book_id).values('case_id'))  # 去合集对应的用例id
        list_case_id = eval(case_id[0]['case_id'])

        print(list_case_id)
        data = ''  # 保存测试结果变量
        for x in range(len(list_case_id)):
            method.modify_config('test', 'id', str(list_case_id[x]))  # 循环更新config中用例id
            case = run.TestOperate()  # 实例化unittest对象
            test_result = case.test_report()
            print(test_result.result)
            TestCases.objects.filter(id=list_case_id[x]).update(case_status=test_result.result[0][0])  # 更新用例状态
            TestCases.objects.filter(id=list_case_id[x]).update(time=method.get_now_date())  # 更新用例执行时间
            if test_result.result[0][0] == 0 or test_result.result[0][0] == 1:
                res2 = eval(str.split(test_result.result[0][2], '\n')[1])
                if res2['message'] is None:
                    res = {
                        "id": x,
                        "code": test_result.result[0][0],
                        "msg": res2['code']
                    }
                    data = str(res) + ',' + data
                else:
                    res = {
                        "id": x,
                        "code": test_result.result[0][0],
                        "msg": res2['message']
                    }
                    data = str(res) + ',' + data
            elif test_result.result[0][0] == 2:
                res = {
                    "id": x,
                    "code": test_result.result[0][0],
                    "msg": '系统异常'
                }
                data = str(res) + ',' + data
            result = list(eval(data))

        res = {
            "code": '0',
            "msg": result
        }
        CaseBook.objects.filter(id=book_id).update(run_time=method.get_now_datetime())  # 更新测试集执行时间
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


# 执行业务流测试合集
@csrf_exempt
def run_business_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('bookId')
        status = CaseBook.objects.filter(id=book_id)[0].book_status
        if status == '3':
            res = {
                "code": '0',
                "msg": '该集合执行中，请稍后去再试'
            }
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
        else:
            # method.assembly_data(book_id, 9)
            CaseBook.objects.filter(id=book_id).update(book_status='3')
            runner = run.TestOperate()
            result = runner.test_business_report(book_id)
            print(result.result)
            res = {
                "code": '0',
                "msg": 'ok'
            }
            CaseBook.objects.filter(id=book_id).update(run_time=method.get_now_datetime())  # 更新测试集执行时间
            try:
                print(result.result[0][0])
            except BaseException as e:
                print('报告异常', e)
                CaseBook.objects.filter(id=book_id).update(book_status=1)
            else:
                CaseBook.objects.filter(id=book_id).update(book_status=result.result[0][0])     # 更新合集状态
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def system(request):
    return render(request, 'system.html')


@csrf_exempt
def system_list(request):
    systems = Systems.objects.all()
    systems_list=[]
    for i in systems:
        systems_dict = {}
        systems_dict["system_id"] = str(i.system_id)
        systems_dict["system_name"] = str(i.system_name)
        systems_dict["system_desc"] = str(i.system_desc)
        systems_list.append(systems_dict)

    query_data = {
        "code": 0,
        "msg": "系统信息数据查询成功",
        "count": systems.count(),
        "data": systems_list}

    # "data": { "item": systems_list }}
    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def save_system(request):
    system_name = request.POST.get('system_name')
    system_desc = request.POST.get('system_desc')

    Systems.objects.create(system_name=system_name, system_desc=system_desc)
    print(Systems.objects.filter(system_id=1))
    return HttpResponse(json.dumps("success", ensure_ascii=False), charset='utf-8')

@csrf_exempt
def delete_system(request):
    system_id = request.POST.get('system_id')
    Systems.objects.filter(system_id=system_id).delete()
    return HttpResponse(json.dumps("success", ensure_ascii=False), charset='utf-8')

@csrf_exempt
def update_system(request):
    if request.method == 'POST':
        system_id = request.POST.get('systemId')
        system_name = request.POST.get('systemName')
        system_brief = request.POST.get('systemBrief')

        try:
            the_system = Systems.objects.filter(system_id=system_id)
            print(the_system[0].system_name)
            print(the_system[0].system_desc)

            the_system.update(system_name=system_name,system_desc=system_brief)
            the_system.save()

        except TestCases.DoesNotExist:
            res = {
                "code": '1',
                "msg": "请求数据不存在"
            }
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')

        finally:
            res = {
                "code": '0',
                "msg": "数据更新成功"
            }
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')

@csrf_exempt
def loading_book_list(request):
    books = CaseBook.objects.all()
    books_count = CaseBook.objects.count()

    books_list = []
    for i in books:
        books_dict = {}
        books_dict["book_id"] = str(i.id)
        books_dict["book_name"] = str(i.book_name)
        books_dict["run_time"] = str(i.run_time)
        books_dict["update_time"] = str(i.update_time)
        books_dict["case_id"] = str(i.case_id)
        books_dict["book_brief"] = str(i.book_brief)
        books_list.append(books_dict)

    print("测试集列表: %s" %books_list)

    all_data = {
          "code": '0',
          "msg": "获取列表成功",
          "count": books_count,
          "data": books_list}

    return HttpResponse(json.dumps(all_data, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def report(request):
    return render(request, 'report.html')

@csrf_exempt
def report_list(request):
    # 获取当前请求页码
    page = request.GET.get('page')
    # 获取前端 tabel.render下的limit
    row = request.GET.get('limit')
    # 计算单次返回的列表区间
    i = (int(page) - 1) * int(row)
    j = (int(page) - 1) * int(row) + int(row)
    # print(i,j)
    # 倒序排列
    reports = Report.objects.all().order_by('-time')
    total = reports.count()
    # print(total)
    reports = reports[i:j]

    report_list = []
    for i in reports:
        report_dict = dict()
        report_dict["report_id"] = str(i.id)
        report_dict["report_name"] = str(i.report_name)
        report_dict["time"] = i.time.strftime("%Y-%m-%d %H:%M:%S")
        if i.status == '0':
            report_dict["status"] = '<span style="color:#32CD32">' + '成功' + '</span>'
        else:
            report_dict["status"] = '<span style="color:#FF6347">' + '失败' + '</span>'
        report_dict["case_name"] = str(i.case_name)
        report_list.append(report_dict)

    query_data = {
        "code": '0',
        "msg": "报告查询成功",
        "count": total,
        "data": report_list}

    # "data": { "item": systems_list }}
    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def read_report(request):
    reports = 'report/%s' % request.GET.get('report_name')
    print(reports)
    return render(request, f'{reports}')

# @csrf_exempt
# def query_hosts(request):
#     # 获取当前请求页码
#     page = request.GET.get('page')
#     # 获取前端 tabel.render下的limit
#     row = request.GET.get('limit')
#     # 计算单次返回的列表区间
#     i = (int(page) - 1) * int(row)
#     j = (int(page) - 1) * int(row) + int(row)
#     # print(i,j)
#
#     print('查询全部数据.')
#     hosts = Hosts.objects.all()
#
#     total = hosts.count()
#     hosts = hosts[i:j]
#     resultdict ={}
#     resultdict['total'] = total
#
#     hosts_list = []
#     for i in hosts:
#         hosts_dict = {}
#         hosts_dict["id"] = str(i.id)
#         hosts_dict["name"] = str(i.hosts_name)
#         hosts_dict["content"] = str(i.hosts_content)
#
#         hosts_list.append(hosts_dict)
#
#     print("记录个数共: %s" %total)
#     print("记录为: %s" %hosts_list)
#
#     query_data = {
#         "code": 0,
#         "msg": "数据查询成功",
#         "count": total,
#         "data": hosts_list}
#
#     return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
#
#
# @csrf_exempt
# def host_list(request):
#     hosts = Hosts.objects.all()
#     hosts_list = []
#     for i in hosts:
#         hosts_dict = dict()
#         hosts_dict["host_id"] = str(i.id)
#         hosts_dict["host_name"] = str(i.hosts_name)
#
#         hosts_list.append(hosts_dict)
#
#     query_data = {
#         "code": 0,
#         "msg": "系统信息数据查询成功",
#         "data": hosts_list}
#
#     # "data": { "item": systems_list }}
#     return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
#
# @csrf_exempt
# def add_hosts(request):
#     if request.method == 'POST':
#         hosts_name = request.POST.get('hostName')
#         hosts_content = request.POST.get('hostContent')
#
#         Hosts.objects.create(hosts_name=hosts_name,hosts_content=hosts_content)
#         res = {
#             "code": '0',
#             "msg": "数据新增成功"
#         }
#
#         # print(type(json.dumps(res)))
#         return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
#     else:
#         return HttpResponse('请求异常,执行失败')
#
# @csrf_exempt
# def delete_hosts(request):
#     if request.method == 'POST':
#         hosts_id = request.POST.get('hostsId')
#         Hosts.objects.filter(id=hosts_id).delete()
#         res = {
#             "code": '0',
#             "msg": "数据删除成功"
#         }
#         return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
#     else:
#         return HttpResponse('请求异常,执行失败')
#
# @csrf_exempt
# def update_hosts(request):
#     if request.method == 'POST':
#         id = request.POST.get('id')
#         hosts_name = request.POST.get('hostName')
#         hosts_content = request.POST.get('hostContent')
#         print(id)
#         try:
#             the_hosts = Hosts.objects.filter(id=id)
#             print(the_hosts[0].hosts_name)
#             the_hosts.update(hosts_name=hosts_name,hosts_content=hosts_content)
#             the_hosts.save()
#
#         except Hosts.DoesNotExist:
#             res = {
#                 "code": '1',
#                 "msg": "请求数据不存在"
#             }
#             return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
#
#         finally:
#             res = {
#                 "code": '0',
#                 "msg": "数据更新成功"
#             }
#             return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
#     else:
#         return HttpResponse('请求异常,执行失败')


# 替换域名
@csrf_exempt
def save_name(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        old_name = request.POST.get('old_name')
        new_name = request.POST.get('new_name')

        books = CaseBook.objects.filter(id=book_id)
        query_data = dict
        cases_id = books[0].case_id
        print(eval(cases_id))
        if cases_id == '':
            query_data = {
                "code": '1',
                "msg": "请先添加用例",
            }
        else:
            result = ''
            cases_id = eval(cases_id)
            for i in range(len(cases_id)):
                case = TestCases.objects.filter(id=cases_id[i])
                url = case[0].case_url
                if old_name in url:
                    url = url.replace(old_name, new_name)
                    print(url)
                    TestCases.objects.filter(id=cases_id[i]).update(case_url=url)
                else:
                    result += case[0].case_name + ','
            print(result)
            if result == '':
                query_data = {
                    "code": '0',
                    "msg": '修改成功',
                }
            else:
                query_data = {
                    "code": '1',
                    "msg": result+'用例域名未修改成功',
                }
        return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')
    else:
        query_data = {
            "code": '1',
            "msg": "请求异常,执行失败",
        }
        return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def attachments(request):
    return render(request, 'attachments.html')


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        try:
            img = request.FILES.getlist('file')  # 取文件列表
            pwd = method.get_program_path()+'\\attachments\\'
            files = Attachments.objects.all()

            for x in range(len(img)):
                status = ''
                f = open(os.path.join(pwd, img[x].name), 'wb')
                for chunk in img[x].chunks():
                    f.write(chunk)
                for i in files:
                    if img[x].name == i.attachments_name:
                        status = '1'
                f.close()
                if status != '1':
                    Attachments.objects.create(attachments_name=img[x].name)
        except BaseException as e:
            query_data = {
                "code": '1',
                "msg": "上传失败,{}".format(e),
            }
        else:
            query_data = {
                "code": '0',
                "msg": "上传成功",
            }
    else:
        query_data = {
            "code": '0',
            "msg": "上传异常",
        }
    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def query_attachments(request):
    page = request.GET.get('page')
    # 获取前端 tabel.render下的limit
    row = request.GET.get('limit')
    # 计算单次返回的列表区间
    i = (int(page) - 1) * int(row)
    j = (int(page) - 1) * int(row) + int(row)

    files = Attachments.objects.all()
    total = files.count()
    files = files[i:j]
    resultdict ={}
    resultdict['total'] = total

    files_list = []
    for i in files:
        files_dict = {}
        files_dict["id"] = str(i.id)
        files_dict["name"] = str(i.attachments_name)

        files_list.append(files_dict)

    print("记录个数共: %s" %total)
    print("记录为: %s" %files_list)

    query_data = {
        "code": 0,
        "msg": "数据查询成功",
        "count": total,
        "data": files_list}

    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def query_relate_attachment(request):
    book_id = request.GET.get('book_id')
    case_id = request.GET.get('case_id')

    page = request.GET.get('page')
    # 获取前端 tabel.render下的limit
    row = request.GET.get('limit')
    # 计算单次返回的列表区间
    i = (int(page) - 1) * int(row)
    j = (int(page) - 1) * int(row) + int(row)

    files = AttachmentsCase.objects.filter(book_id=book_id, case_id=case_id)
    total = files.count()
    files = files[i:j]
    result_dict = dict()
    result_dict['total'] = total

    files_list = []
    for i in files:
        files_dict = dict()
        files_dict["id"] = str(i.id)
        files_dict["book_id"] = str(i.book_id)
        files_dict["case_id"] = str(i.case_id)
        files_dict["attachments_id"] = str(i.attachments_id)
        file_name = Attachments.objects.filter(id=str(i.attachments_id))
        file_name = file_name[0].attachments_name
        files_dict["name"] = file_name
        files_dict["send_name"] = str(i.send_name)
        files_list.append(files_dict)

    print("记录个数共: %s" % total)
    print("记录为: %s" % files_list)

    query_data = {
        "code": 0,
        "msg": "数据查询成功",
        "count": total,
        "data": files_list}

    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


@csrf_exempt
def delete_attachments(request):
    if request.method == 'POST':
        attachments_id = request.POST.get('attachmentsId')
        attachments_name = request.POST.get('attachmentsName')
        files_id = AttachmentsCase.objects.all()
        status = ''
        for x in files_id:
            if attachments_id == x.attachments_id:
                status = '1'
        if status == '1':
            res = {
                "code": '0',
                "msg": "该数据已被关联"
            }
        else:
            Attachments.objects.filter(id=attachments_id).delete()
            pwd = method.get_program_path() + '\\attachments\\' + attachments_name
            os.remove(pwd)
            res = {
                "code": '0',
                "msg": "数据删除成功"
            }
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def relate_attachment(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        case_id = request.POST.get('case_id')
        attachment_id = request.POST.get('attachment_id')
        send_name = request.POST.get('send_name')
        relate = AttachmentsCase.objects.filter(book_id=book_id, case_id=case_id)
        status = ''
        for x in relate:
            if attachment_id == x.attachments_id:
                status = '1'
                break
        if status == '1':
            res = {
                "code": '1',
                "msg": "该附件已关联"
            }
        else:
            AttachmentsCase.objects.create(book_id=book_id, case_id=case_id, attachments_id=attachment_id, send_name=send_name)
            res = {
                "code": '0',
                "msg": "附件关联成功"
            }
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def remove_attachment(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        case_id = request.POST.get('case_id')
        attachment_id = request.POST.get('attachment_id')
        print(book_id, case_id, attachment_id)
        AttachmentsCase.objects.filter(book_id=book_id, case_id=case_id, attachments_id=attachment_id).delete()
        res = {
            "code": '0',
            "msg": "解除关联成功"
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')

@csrf_exempt
def load_databases(request):
    file_name = "config\config.ini"
    ex_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),file_name)
    print(ex_path)
    output = open(ex_path, 'r', encoding='utf-8')

    data = output.readlines()
    data = '<br>'.join(data)
    # print(data)
    output.close()
    res = {'code': '0',
           'data': data,
           }
    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def save_databases(request):
    if request.method == 'POST':
        database_content = request.POST.get('content')
        # print(database_content)
        file_name = "CreditApplication\config\config.ini"
        ex_path = os.path.join(os.path.abspath('.'),file_name)
        print(ex_path)
        with open(ex_path, 'w', encoding='utf-8') as f:
            f.write(database_content)
        f.close()
        res = {'code': '0',
               'msg': "文件写入成功."
               }
    else:
        res = {'code': '0',
               'msg': "文件打开异常,写入文件失败."
               }

    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def load_databases_backup(request):
    file_name = r"config\backup.txt"
    ex_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),file_name)
    print(ex_path)
    output = open(ex_path, 'r', encoding='utf-8')
    data = output.readlines()
    data = '<br>'.join(data)
    print(data)
    output.close()

    res = {'code': '0',
           'data': data,
           }
    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def save_databases_backup(request):
    if request.method == 'POST':
        backup_content = request.POST.get('backup_content')
        # print(database_content)
        file_name = r"config\backup.txt"
        ex_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)
        print(ex_path)
        with open(ex_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
        f.close()
        res = {'code': '0',
               'msg': "备份文件写入成功."
               }
    else:
        res = {'code': '0',
               'msg': "文件打开异常,写入文件失败."
               }

    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def load_hosts_backup(request):
    file_name = r"config\hosts_backup.txt"
    ex_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),file_name)
    print(ex_path)
    output = open(ex_path, 'r', encoding='utf-8')
    data = output.readlines()
    data = '<br>'.join(data)
    print(data)
    output.close()

    res = {'code': '0',
           'data': data,
           }
    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def save_hosts(request):
    if request.method == 'POST':
        database_content = request.POST.get('content')
        # print(database_content)
        sys_type = platform.system()
        if sys_type == "Windows":
            ex_path = "C:\WINDOWS\system32\drivers\etc\HOSTS"
            with open(ex_path, 'w') as f:
                f.write(database_content)
            f.close()
            res = {'code': '0',
                   'msg': "windows_hosts写入成功."}
        elif sys_type == "Linux":
            ex_path = r"/etc/hosts"
            print(ex_path)
    else:
        res = {'code': '0',
               'msg': "文件打开异常,写入文件失败."
               }

    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')

@csrf_exempt
def save_hosts_backup(request):
    if request.method == 'POST':
        backup_content = request.POST.get('backup_content')
        # print(database_content)
        file_name = r"config\hosts_backup.txt"
        ex_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)
        print(ex_path)
        with open(ex_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
        f.close()
        res = {'code': '0',
               'msg': "备份文件写入成功."
               }
    else:
        res = {'code': '0',
               'msg': "文件打开异常,写入文件失败."
               }

    return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')


#  添加定时任务
@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        task_config = request.POST.get('task_config')
        if len(Tasks.objects.all()) == 0:
            Tasks.objects.create(book_id=book_id, task_config=task_config)
            res = {
                "code": '0',
                "msg": "数据新增成功"
            }
            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
        else:
            books_id = Tasks.objects.all()[0].book_id
            books_id = books_id + ',' + book_id
            Tasks.objects.all().update(book_id=books_id)
            res = {
                "code": '0',
                "msg": "数据新增成功"
            }

            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


#  更新定时任务
@csrf_exempt
def update_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        book_id = request.POST.get('book_id')
        task_config = request.POST.get('task_config')
        Tasks.objects.filter(id=task_id).update(book_id=book_id, task_config=task_config)
        res = {
            "code": '0',
            "msg": "数据更新成功"
        }

        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


@csrf_exempt
def query_task(request):
    # 获取当前请求页码
    page = request.GET.get('page')
    # 获取前端 tabel.render下的limit
    row = request.GET.get('limit')
    # 计算单次返回的列表区间
    i = (int(page) - 1) * int(row)
    j = (int(page) - 1) * int(row) + int(row)

    book = Tasks.objects.all()

    total = book.count()
    books = book[i:j]
    resultdict ={}
    resultdict['total'] = total

    books_list = []
    for i in books:
        books_dict = {}
        books_dict["taskId"] = str(i.id)
        books_dict["bookId"] = str(i.book_id)
        books_dict["taskConfig"] = str(i.task_config)
        # book_name = CaseBook.objects.filter(id=str(i.book_id))[0].book_name
        # books_dict["bookName"] = book_name
        books_list.append(books_dict)

    print("记录个数共: %s" % total)
    print("记录为: %s" % books_list)

    query_data = {
        "code": 0,
        "msg": "数据查询成功",
        "count": total,
        "data": books_list}

    return HttpResponse(json.dumps(query_data, ensure_ascii=False), charset='utf-8')


def job():
    url = 'http://127.0.0.1:5527/runBusinessBook/'
    books_id = Tasks.objects.all()[0].book_id
    data_list = list()

    for i in range(len(eval(books_id))):
        data = dict()
        data['bookId'] = eval(books_id)[i]
        data_list.append(data)
    # headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    for x in range(len(data_list)):
        requests.post(url=url, data=data_list[x])


# scheduler = BlockingScheduler()
scheduler = BackgroundScheduler()


#  运行定时任务
@csrf_exempt
def run_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('taskId')
        book_id = request.POST.get('bookId')
        task_config = request.POST.get('taskConfig')
        task_config = eval(task_config)

        scheduler.add_job(job, 'cron', day_of_week=task_config[0], hour=task_config[1]
                          , minute=task_config[2], id='job_{}'.format(task_id))

        scheduler.start()
        res = {
            "code": '0',
            "msg": "数据更新成功"
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


#  查询定时任务
@csrf_exempt
def show_task(request):
    if request.method == 'POST':
        b = scheduler.get_jobs()
        if len(b) > 0:
            res = {
                "code": '0',
                "msg": '任务已启动'
            }

            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
        else:
            res = {
                "code": '0',
                "msg": '任务未启动'
            }

            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')


#  停止定时任务
@csrf_exempt
def stop_task(request):
    if request.method == 'POST':
        b = scheduler.get_jobs()
        if len(b) > 0:
            scheduler.shutdown(wait=False)
            res = {
                "code": '0',
                "msg": '任务停止'
            }

            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
        else:
            res = {
                "code": '0',
                "msg": '无任务启动'
            }

            return HttpResponse(json.dumps(res, ensure_ascii=False), charset='utf-8')
    else:
        return HttpResponse('请求异常,执行失败')

