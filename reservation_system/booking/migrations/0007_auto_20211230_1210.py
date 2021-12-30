# Generated by Django 3.2 on 2021-12-30 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20211229_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='user',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='guest',
        ),
        migrations.AddField(
            model_name='bill',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]