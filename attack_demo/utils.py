from attack_demo.models import *

def read_dev_and_topo():
    device = {}
    conns = {}
    results = {}
    d_all = Device.objects.all()
    for d in d_all:
        d_id = d.serializable_value('device_id')
        d_name = d.serializable_value('device_name')
        for f in device_fields:
            device[f] = d.serializable_value(f)
        conn = DeviceTopology.objects.filter(device_name=d_name)
        if conn.count() == 0:
            pass
        else:
            conn = conn[0]
            for f in devicetopology_fields:
                if f != 'device_name':
                    conns[f] = conn.serializable_value(f)
        device['device_conns'] = conns
        results['device' + str(d_id)] = device
        device = {}
        conns = {}
    return results


def read_tools_and_args():
    tool = {}
    args = []
    results = {}
    t_all = AttackTool.objects.all().values()
    for t in t_all:
        tool = t
        for a in AttackArg.objects.filter(attack_type=t['attack_type']):
            args.append(a.attack_arg)
        tool['attack_arg'] = args
        args = []
        results['tool' + t['attack_id']] = tool
    return results


def read_demotopo():
    alldev = Device.objects.all()
    results = {}
    connsip = []
    connsdev = []
    for dev in alldev:
        conns = DeviceTopology.objects.filter(device_name=dev.device_name).values()[0]
        conns.pop('device_name_id')
        for co in conns.values():
            if co != None:
                connsip.append(co)
        for co in connsip:
            obj = Device.objects.get(device_ip=co)
            connsdev.append(obj.device_name)
        results[dev.device_name] = connsdev
        connsip = []
        connsdev = []
    return results


# device_fields = [f.name for f in Device._meta.fields]
# [
#     'device_id',
#     'device_name',
#     'device_ip',
#     'device_type',
#     'device_level',
#     'device_createtime',
#     'device_brand',
#     'device_desc'
# ]
# The DeviceTopology table's fields.
# devicetopology_fields = [f.name for f in DeviceTopology._meta.fields]
# [
#     'device_name',
#     'interface1',
#     'interface2',
#     'interface3',
#     'interface4',
#     'interface5',
#     'interface6',
#     'interface7'
# ]
# The AttackHistory table's fields.
# attackhistory_fields = [f.name for f in AttackHistory._meta.fields]
# [
#     'record_id',
#     'create_time',
#     'attack_type',
#     'attack_src',
#     'attack_dst',
#     'threaten_level'
# ]
