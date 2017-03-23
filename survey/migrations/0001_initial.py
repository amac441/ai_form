# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerBase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('docFile', models.FileField(blank=True, upload_to='Data_Files')),
                ('author', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('required', models.BooleanField()),
                ('question_type', models.CharField(default='text', max_length=200, choices=[('text', 'text'), ('radio', 'radio'), ('select', 'select'), ('select-multiple', 'Select Multiple'), ('integer', 'integer')])),
                ('choices', models.TextField(null=True, blank=True, help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')),
                ('category', models.ForeignKey(null=True, blank=True, to='survey.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(null=True, verbose_name='Idea Name', blank=True, max_length=400)),
                ('interview_uuid', models.CharField(verbose_name='Interview unique identifier', max_length=36)),
                ('filelist', models.TextField(null=True, blank=True)),
                ('draft', models.BooleanField(default=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AnswerInteger',
            fields=[
                ('answerbase_ptr', models.OneToOneField(serialize=False, to='survey.AnswerBase', parent_link=True, auto_created=True, primary_key=True)),
                ('body', models.IntegerField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerRadio',
            fields=[
                ('answerbase_ptr', models.OneToOneField(serialize=False, to='survey.AnswerBase', parent_link=True, auto_created=True, primary_key=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerSelect',
            fields=[
                ('answerbase_ptr', models.OneToOneField(serialize=False, to='survey.AnswerBase', parent_link=True, auto_created=True, primary_key=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerSelectMultiple',
            fields=[
                ('answerbase_ptr', models.OneToOneField(serialize=False, to='survey.AnswerBase', parent_link=True, auto_created=True, primary_key=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.CreateModel(
            name='AnswerText',
            fields=[
                ('answerbase_ptr', models.OneToOneField(serialize=False, to='survey.AnswerBase', parent_link=True, auto_created=True, primary_key=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
            bases=('survey.answerbase',),
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(null=True, to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='comment',
            name='response',
            field=models.ForeignKey(to='survey.Response', related_name='comments'),
        ),
        migrations.AddField(
            model_name='category',
            name='survey',
            field=models.ForeignKey(to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='question',
            field=models.ForeignKey(to='survey.Question'),
        ),
        migrations.AddField(
            model_name='answerbase',
            name='response',
            field=models.ForeignKey(to='survey.Response'),
        ),
    ]
