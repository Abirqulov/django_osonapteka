# Generated by Django 3.2.6 on 2021-08-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210811_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='price',
            field=models.CharField(default=2, max_length=120),
            preserve_default=False,
        ),
    ]
