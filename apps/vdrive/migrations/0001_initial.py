# Generated by Django 3.0 on 2019-12-26 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Processing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='creation date')),
                ('source_type', models.URLField(max_length=250, unique=True, verbose_name='source of the file')),
            ],
        ),
        migrations.CreateModel(
            name='VideoProc',
            fields=[
                ('source_id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name=' id of video in the source')),
                ('status_video', models.CharField(choices=[('WT', 'Waiting to upload'), ('InPr', 'In progress of uploading'), ('ErrorMes', 'Error message'), ('SuccUp', 'Successfully Uploaded')], default='WT', max_length=8)),
                ('error_message_video', models.CharField(default='Error. Something went wrong', max_length=250)),
                ('youtube_id', models.CharField(max_length=250, unique=True, verbose_name=' id of youtube uploaded video')),
                ('youtube_link', models.URLField(max_length=250, unique=True, verbose_name='link of the video from youtube')),
                ('proc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vdrive.Processing')),
            ],
        ),
    ]
