# Generated by Django 2.1.2 on 2019-01-17 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fastrunner', '0002_auto_20190116_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='任务名称')),
                ('identity', models.CharField(max_length=100, unique=True, verbose_name='任务ID')),
                ('send_type', models.IntegerField(choices=[(1, '始终发送'), (2, '仅失败发送'), (3, '从不发送')], default=3, verbose_name='发送策略')),
                ('config', models.TextField(verbose_name='任务分配')),
                ('receiver', models.CharField(max_length=2048, null=True, verbose_name='接受人')),
                ('copy', models.CharField(max_length=2048, null=True, verbose_name='抄送人')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fastrunner.Project', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '定时任务',
                'db_table': 'Schedule',
            },
        ),
    ]