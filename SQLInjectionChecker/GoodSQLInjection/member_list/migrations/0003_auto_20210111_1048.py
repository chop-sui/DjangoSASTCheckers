# Generated by Django 3.1.5 on 2021-01-11 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member_list', '0002_auto_20210110_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]