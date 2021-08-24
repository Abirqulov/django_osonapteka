# Generated by Django 3.2.6 on 2021-08-24 11:30

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('image', models.ImageField(upload_to='static/images')),
                ('description', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('slug', models.SlugField(blank=True, max_length=125, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='static/drug_images')),
                ('description_uz', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('description_ru', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('barcode', models.CharField(blank=True, max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InternationalName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=225)),
                ('name_ru', models.CharField(max_length=225)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PharmGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=150)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReleaseForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=150)),
                ('name_ru', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='regions',
            name='parent',
        ),
    ]