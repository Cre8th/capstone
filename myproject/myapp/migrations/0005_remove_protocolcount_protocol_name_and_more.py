# Generated by Django 5.0.4 on 2024-05-20 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_protocolcount_delete_protocolpacketcount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protocolcount',
            name='protocol_name',
        ),
        migrations.AddField(
            model_name='protocolcount',
            name='protocol',
            field=models.CharField(default='default_value', max_length=50),
        ),
    ]