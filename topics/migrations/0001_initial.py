# Generated by Django 5.0 on 2023-12-30 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='内容')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('source', models.IntegerField(default=1)),
                ('like', models.IntegerField(default=0)),
                ('temp_name', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'verbose_name_plural': 'talks',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forward', models.IntegerField(default=1)),
                ('source', models.IntegerField(default=1)),
                ('content', models.CharField(max_length=200, verbose_name='你的评论')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('like', models.IntegerField(default=0)),
                ('temp_name', models.CharField(blank=True, max_length=1, null=True)),
                ('talk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.talk')),
            ],
            options={
                'verbose_name_plural': 'responses',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='主题')),
                ('content', models.TextField(max_length=2000, verbose_name='内容')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('like', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.ouruser')),
            ],
        ),
        migrations.AddField(
            model_name='talk',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.topic'),
        ),
    ]
