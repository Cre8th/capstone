# Generated by Django 5.0.4 on 2024-06-06 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_delete_protocol_delete_protocolcount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packet_type', models.CharField(max_length=5)),
                ('src_port', models.CharField(max_length=7)),
                ('dest_port', models.CharField(max_length=7)),
                ('src_IP', models.CharField(max_length=20)),
                ('dest_IP', models.CharField(max_length=20)),
                ('data', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('src', models.GenericIPAddressField()),
            ],
        ),
    ]