# Generated by Django 2.2.1 on 2019-05-07 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190507_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='read_num',
            field=models.IntegerField(default=0),
        ),
    ]
