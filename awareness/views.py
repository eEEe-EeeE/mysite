from django.shortcuts import render

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from awareness.models import *
# Create your views here.

@csrf_exempt
@require_http_methods(['POST'])
def addVuln(request):
    info = request.POST.dict()
    SystemVuln.objects.create(**info)
    results = {
        'msg': '添加系统漏洞记录成功',
        'detail': info
    }
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(['POST'])
def dropVuln(request):
    v_id = request.POST['id']
    SystemVuln.objects.get(device_name=name).delete()
    results = {
        'msg': '删除系统漏洞记录成功',
        'device_name': v_id
    }
    if not SystemVuln.objects.all().exists():
        reset.reset_auto_increment('awareness_systemvuln')
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(['POST'])
def updateVuln(request):
    info = {}
    v_id = request.POST['id']
    for k, v in request.POST.items():
        if k != 'id':
            info[k[4:]] = v
    SystemVuln.objects.filter(pk=v_id).update(**info)
    results = {
        'msg': '更新系统漏洞记录成功',
        'detail': info
    }
    return JsonResponse(results)

@require_http_methods(['GET'])
def getVuln_pie(request):
    low_num = SystemVuln.objects.filter(vulnlevel='1').count()
    middle_num = SystemVuln.objects.filter(vulnlevel='2').count()
    high_num = SystemVuln.objects.filter(vulnlevel='3').count()
    results = {
        '低危': str(low_num),
        '中危': str(middle_num),
        '高危': str(high_num),
        '总数': str(low_num + middle_num + high_num)
    }
    return JsonResponse(results)


@require_http_methods(['GET'])
def getVuln_line(request):
    vulnlist = SystemVuln.objects.values('vuln_createtime').distinct().order_by('vuln_createtime')
    vulntime = [d['vuln_createtime'] for d in vulnlist]
    results = {}
    detail = {}
    for t in vulntime:
        low_num = SystemVuln.objects.filter(vuln_createtime=t, vulnlevel='1').count()
        middle_num = SystemVuln.objects.filter(vuln_createtime=t, vulnlevel='2').count()
        high_num = SystemVuln.objects.filter(vuln_createtime=t, vulnlevel='3').count()
        detail = {
            '低危': str(low_num),
            '中危': str(middle_num),
            '高危': str(high_num),
            '总数': str(low_num + middle_num + high_num)
        }
        results[t] = detail
    return JsonResponse(results)
