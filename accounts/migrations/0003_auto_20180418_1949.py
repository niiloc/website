# Generated by Django 2.0.3 on 2018-04-18 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180417_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='user_profile',
            field=models.CharField(max_length=100),
        ),
    ]