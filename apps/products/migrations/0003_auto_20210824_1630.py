# Generated by Django 3.2.6 on 2021-08-24 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_auto_20210824_1630'),
        ('products', '0002_auto_20210824_1630'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Regions',
        ),
        migrations.AddField(
            model_name='drug',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.category'),
        ),
        migrations.AddField(
            model_name='drug',
            name='international_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.internationalname'),
        ),
        migrations.AddField(
            model_name='drug',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.manufacturer'),
        ),
        migrations.AddField(
            model_name='drug',
            name='pharm_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.pharmgroup'),
        ),
        migrations.AddField(
            model_name='drug',
            name='release_form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.releaseform'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='childs', to='products.category'),
        ),
    ]