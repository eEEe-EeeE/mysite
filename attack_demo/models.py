from django.db import models

# Create your models here.
class Device(models.Model):
    D_TYPE = (
        ('router', 'router'),
        ('switch', 'switch'),
        ('server', 'server'),
        ('host', 'host'),
        ('firewall', 'firewall'),
        ('hub', 'hub'),
        ('RTU', 'RTU'),
        ('PLC', 'PLC'),
        ('camera', 'camera'),
        ('meter', 'meter'),
        ('machine', 'machine')
    )
    device_id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=30, unique=True)
    device_ip = models.CharField(max_length=15)
    device_type = models.CharField(max_length=10, choices=D_TYPE)
    device_level = models.CharField(max_length=2)
    device_createtime = models.DateTimeField(auto_now_add=True)
    device_brand = models.CharField(max_length=30, null=True, blank=True)
    device_desc = models.CharField(max_length=255, null=True, blank=True)


class DeviceTopology(models.Model):
    device_name = models.OneToOneField(Device, on_delete=models.CASCADE, null=False, blank=False, to_field='device_name', primary_key=True)
    interface1 = models.CharField(max_length=15, null=True, blank=True)
    interface2 = models.CharField(max_length=15, null=True, blank=True)
    interface3 = models.CharField(max_length=15, null=True, blank=True)
    interface4 = models.CharField(max_length=15, null=True, blank=True)
    interface5 = models.CharField(max_length=15, null=True, blank=True)
    interface6 = models.CharField(max_length=15, null=True, blank=True)
    interface7 = models.CharField(max_length=15, null=True, blank=True)


class AttackTool(models.Model):
    A_TYPE = (
        ('NetworkMonitoring', 'NetworkMonitoring'),
        ('NetworkScanning', 'NetworkScanning'),
        ('ICPMredirect', 'ICPMredirect'),
        ('RouteSpoofing', 'RouteSpoofing'),
        ('ARPspoofing', 'ARPspoofing'),
        ('PortScanning', 'PortScanning'),
        ('SYNflooding', 'SYNflooding'),
        ('TCPspoofing', 'TCPspoofing'),
        ('OutOfBuffer', 'OutOfBuffer'),
        ('Virus&TrojanHorse', 'Virus&TrojanHorse'),
        ('SQLinjection', 'SQLinjection'),
        ('DDoS', 'DDoS')
    )
    attack_id = models.AutoField(primary_key=True)
    attack_type = models.CharField(max_length=30, unique=True, choices=A_TYPE)
    attack_level = models.CharField(max_length=2, null=True)
    attack_desc = models.CharField(max_length=255, null=True, blank=True)


class AttackArg(models.Model):
    attack_type = models.ForeignKey(AttackTool, on_delete=models.CASCADE, null=False, blank=False, to_field='attack_type')
    attack_arg = models.CharField(max_length=30)


class AttackHistory(models.Model):
    record_id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    attack_type = models.CharField(max_length=30)
    attack_src = models.CharField(max_length=30)
    attack_dst = models.CharField(max_length=30)
    threaten_level = models.CharField(max_length=2)


class AttackScript(models.Model):
    title = models.CharField(null=False, blank=False, max_length=180)
    script_type = models.CharField(max_length=30)
    platform = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    published = models.DateField(auto_now=False, auto_now_add=False)
    vuln_sorftware = models.CharField(max_length=40)
    download = models.CharField(unique=True, null=False, blank=False, max_length=150)