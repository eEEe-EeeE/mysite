from django.shortcuts import render

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from attack_demo.models import *
from attack_demo import reset, utils, graph
import os, json, copy
# Create your macros here.

# The Device table's fields.
device_fields = [f.name for f in Device._meta.fields]
# The DeviceTopology table's fields.
devicetopology_fields = [f.name for f in DeviceTopology._meta.fields]
# The AttackHistory table's fields.
attackhistory_fields = [f.name for f in AttackHistory._meta.fields]
# The number of a device's interface.
INTERFACE_NUM = 7
# File superior directory.
DIR = os.path.dirname(__file__)
# Error infomation.
error_results = {
                    'msg': '',
                    'detail': {
                        'error_code': 'ERR_000',
                        'error_msg': 'system internal error.'
                    }
                }

# Create your views here.

### 设备管理部分
@csrf_exempt
@require_http_methods(['POST'])
def addDevice(request):
    info = request.POST.dict()
    Device.objects.create(**info)
    results = {
        'msg': '添加设备成功',
        'detail': info
    }
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(['POST'])
def addConnection(request):
    conns = request.POST.dict()
    name = conns.pop('device_name')
    obj = Device.objects.get(device_name=name)
    if not DeviceTopology.objects.filter(device_name=name).exists():
        DeviceTopology.objects.create(device_name=obj, **conns)
    else:
        for conn in conns.keys():
            if DeviceTopology.objects.get(device_name=name).serializable_value(conn) != None:
                error_results['msg'] = '操作失败'
                return JsonResponse(error_results)
        DeviceTopology.objects.filter(device_name=name).update(**conns)
    info = request.POST.dict()
    results = {
        'msg': '添加设备连接成功',
        'detail': info
    }
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(['POST'])
def dropDevice(request):
    name = request.POST['device_name']
    Device.objects.get(device_name=name).delete()
    results = {
        'msg': '删除设备成功',
        'device_name': name
    }
    if not Device.objects.all().exists():
        reset.reset_auto_increment('attack_demo_Device')
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(['POST'])
def dropConnection(request):
    name = request.POST['device_name']
    conns = request.POST.getlist('interface_id')
    inter_id = {}
    inter_id_print = {}
    not_empty_sign = 0
    if conns == []:
        results = {
            'msg': '删除设备连接成功'
        }
        return JsonResponse(results)
    for iid in range(1, INTERFACE_NUM + 1):
        iid = str(iid)
        inf = 'interface' + iid
        ip = DeviceTopology.objects.get(device_name=name).serializable_value(inf)
        if iid in conns:
            inter_id[inf] = None
            inter_id_print[inf] = ip
        elif ip != None:
            not_empty_sign = 1
    if not not_empty_sign:
        DeviceTopology.objects.get(device_name=name).delete()
    else:
        DeviceTopology.objects.filter(device_name=name).update(**inter_id)
    results = {
        'msg': '删除设备连接成功',
        'detail': inter_id_print
    }
    if not DeviceTopology.objects.all().exists():
        reset.reset_auto_increment('attack_demo_devicetopology')
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(['POST'])
def updateDevice(request):
    info = {}
    name = request.POST['device_name']
    for k, v in request.POST.items():
        if k != 'device_name':
            info['device' + k[3:]] = v
    Device.objects.filter(device_name=name).update(**info)
    results = {
        'msg': '更新设备成功',
        'detail': info
    }
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(['POST'])
def updateConnection(request):
    name = request.POST['device_name']
    info = {}
    for k, v in request.POST.items():
        if k != 'device_name':
            info[k] = v
    if not DeviceTopology.objects.all().exists():
        error_results['msg'] = '设备连接为空,操作失败'
        return JsonResponse(error_results)
    DeviceTopology.objects.filter(device_name=name).update(**info)
    results = {
        'msg': '更新设备连接成功',
        'detail': info
    }
    return JsonResponse(results)


@require_http_methods(['GET'])
def getDeviceList(request):
    devlist = Device.objects.all().values()
    results = {}
    for d in devlist:
        results['device' + str(d['device_id'])] = d
    return JsonResponse(results)


@require_http_methods(['GET'])
def getDeviceDesc(request):
    name = request.GET['device_name']
    dev = Device.objects.get(device_name=name)
    results = {}
    for f in device_fields:
        results[f] = dev.serializable_value(f)
    return JsonResponse(results)


@require_http_methods(['GET'])
def getDeviceConnection(request):
    name = request.GET['device_name']
    dev = Device.objects.get(device_name=name)
    if DeviceTopology.objects.all().exists():
        conn = DeviceTopology.objects.get(device_name=name)
    else:
        error_results['msg'] = '设备连接为空,操作失败'
        return JsonResponse(error_results)
    conns = {}
    for f in devicetopology_fields:
        if f != 'device_name':
            conns[f] = conn.serializable_value(f)
    results = {
        'device_name': dev.serializable_value('device_name'),
        'conns': conns
    }
    return JsonResponse(results)


### 攻击工具部分
@csrf_exempt
@require_http_methods(['POST'])
def attackDemo(request):
    acktype = request.POST['attack_type']
    src = request.POST['attack_source']
    dst = request.POST['attack_destination']

    gra = utils.read_demotopo()
    aj = graph.AdjacencyList()
    aj.addGraph(**gra)
    path = aj.showPath(src, dst, 'dijkstra')

    info = {}
    info['source'] = src
    info['destination'] = dst
    info['path'] = path
    hs = {}
    hs['attack_type'] = acktype
    hs['attack_src'] = src
    hs['attack_dst'] = dst
    hs['threaten_level'] = '1'
    obj = AttackHistory.objects.create(**hs)
    hs = {}
    hs = AttackHistory.objects.filter(pk=obj.record_id).values()[0]
    results = {
        'history': hs,
        'detail': info
    }
    return JsonResponse(results)


@require_http_methods(['GET'])
def getAttackArg(request):
    tools = AttackTool.objects.all()
    results = {}
    args = []
    for tool in tools:
        name = tool.attack_type
        tid = tool.attack_id
        for a in AttackArg.objects.filter(attack_type=name):
            args.append(a.attack_arg)
        results['tool' + str(tid)] = {
            'attack_type': name,
            'attack_arg': args
        }
        args = []
    return JsonResponse(results)


@require_http_methods(['GET'])
def getHistories(request):
    hs = AttackHistory.objects.all().values() # [{}, {}]
    results = {}
    for h in hs:
        results['history' + str(h['record_id'])] = h
    return JsonResponse(results)

@csrf_exempt
@require_http_methods(['POST'])
def deleteHistory(request):
    hs = request.POST.getlist('record_id')
    results = {}
    for h in hs:
        info = AttackHistory.objects.filter(pk=int(h)).values()[0]
        results['record' + h] = info
        AttackHistory.objects.get(pk=int(h)).delete()
    if not AttackHistory.objects.all().exists():
        reset.reset_auto_increment('attack_demo_attackhistory')
    return JsonResponse(results)


@require_http_methods(['GET'])
def emptyHistory(request):
    AttackHistory.objects.all().delete()
    reset.reset_auto_increment('attack_demo_attackhistory')
    results = {
        'msg': '清空历史纪录成功'
    }
    return JsonResponse(results)


@require_http_methods(['GET'])
def demoInit(request):
    # results = read_dev_and_topo()
    Device.objects.all().delete()
    DeviceTopology.objects.all().delete()
    reset.reset_auto_increment('attack_demo_Device')
    f = open(DIR + '/initdata.json', encoding='utf-8')
    results = json.loads(f.read())
    info = copy.deepcopy(results)
    conns = {}
    for v in info.values():
        # v.pop('device_id')
        v.pop('device_createtime')
        conns = v.pop('device_conns')
        obj = Device.objects.create(**v)
        DeviceTopology.objects.create(device_name=obj, **conns)
    return JsonResponse(results)


@require_http_methods(['GET'])
def toolsInit(request):
    AttackTool.objects.all().delete()
    AttackArg.objects.all().delete()
    reset.reset_auto_increment('attack_demo_AttackTool')
    reset.reset_auto_increment('attack_demo_AttackArg')
    f = open(DIR + '/inittools.json', encoding='utf-8')
    results = json.loads(f.read())
    info = copy.deepcopy(results)
    args = []
    for tool in info.values():
        args = tool.pop('attack_arg')
        t = AttackTool.objects.create(**tool)
        for a in args:
            t.attackarg_set.create(attack_arg=a)
        args = []
    return JsonResponse(results)


### 攻击脚本部分
@require_http_methods(['GET'])
def scriptsInit(request):
    AttackScript.objects.all().delete()
    reset.reset_auto_increment('attack_demo_AttackScript')
    f = open(DIR + '/initscripts.json', encoding='utf-8')
    results = json.loads(f.read())
    info = copy.deepcopy(results)
    for script in info.values():
        AttackScript.objects.create(**script)
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(['POST'])
def addScript(request):
    info = request.POST.dict()
    AttackScript.objects.create(**info)
    results = {
        'msg': '添加脚本成功',
        'detail': info
    }
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(['POST'])
def deleteScript(request):
    s_id = request.POST['id']
    obj = AttackScript.objects.filter(pk=int(s_id))
    info = obj.values()[0]
    obj.delete()
    results = {
        'msg': '删除脚本成功',
        'detail': info
    }
    if not AttackScript.objects.all().exists():
        reset.reset_auto_increment('attack_demo_AttackScript')
    return JsonResponse(results)


@require_http_methods(['GET'])
def getScripts(request):
    all_sc = AttackScript.objects.all().values() # [{}, {}]
    results = {}
    for sc in all_sc:
        results['script' + str(sc['id'])] = sc
    return JsonResponse(results)