# Generated by Django 3.1.3 on 2022-06-30 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('1', 'Zipcho_Admin'), ('2', 'Contestant')], default='2', max_length=30),
        ),
    ]
