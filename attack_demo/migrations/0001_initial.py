# Generated by Django 2.1.2 on 2018-12-12 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttackArg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attack_arg', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='AttackHistory',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('attack_type', models.CharField(max_length=30)),
                ('attack_src', models.CharField(max_length=30)),
                ('attack_dst', models.CharField(max_length=30)),
                ('threaten_level', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='AttackScript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('script_type', models.CharField(max_length=30)),
                ('platform', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=30)),
                ('published', models.DateField()),
                ('vuln_sorftware', models.CharField(max_length=40)),
                ('download', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttackTool',
            fields=[
                ('attack_id', models.AutoField(primary_key=True, serialize=False)),
                ('attack_type', models.CharField(choices=[('NetworkMonitoring', 'NetworkMonitoring'), ('NetworkScanning', 'NetworkScanning'), ('ICPMredirect', 'ICPMredirect'), ('RouteSpoofing', 'RouteSpoofing'), ('ARPspoofing', 'ARPspoofing'), ('PortScanning', 'PortScanning'), ('SYNflooding', 'SYNflooding'), ('TCPspoofing', 'TCPspoofing'), ('OutOfBuffer', 'OutOfBuffer'), ('Virus&TrojanHorse', 'Virus&TrojanHorse'), ('SQLinjection', 'SQLinjection'), ('DDoS', 'DDoS')], max_length=30, unique=True)),
                ('attack_level', models.CharField(max_length=2, null=True)),
                ('attack_desc', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.AutoField(primary_key=True, serialize=False)),
                ('device_name', models.CharField(max_length=30, unique=True)),
                ('device_ip', models.CharField(max_length=15)),
                ('device_type', models.CharField(choices=[('router', 'router'), ('switch', 'switch'), ('server', 'server'), ('host', 'host'), ('firewall', 'firewall'), ('hub', 'hub'), ('RTU', 'RTU'), ('PLC', 'PLC'), ('camera', 'camera'), ('meter', 'meter'), ('machine', 'machine')], max_length=10)),
                ('device_level', models.CharField(max_length=2)),
                ('device_createtime', models.DateTimeField(auto_now_add=True)),
                ('device_brand', models.CharField(blank=True, max_length=30, null=True)),
                ('device_desc', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceTopology',
            fields=[
                ('device_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='attack_demo.Device', to_field='device_name')),
                ('interface1', models.CharField(blank=True, max_length=15, null=True)),
                ('interface2', models.CharField(blank=True, max_length=15, null=True)),
                ('interface3', models.CharField(blank=True, max_length=15, null=True)),
                ('interface4', models.CharField(blank=True, max_length=15, null=True)),
                ('interface5', models.CharField(blank=True, max_length=15, null=True)),
                ('interface6', models.CharField(blank=True, max_length=15, null=True)),
                ('interface7', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='attackarg',
            name='attack_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attack_demo.AttackTool', to_field='attack_type'),
        ),
    ]
