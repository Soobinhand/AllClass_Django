# Generated by Django 4.0.3 on 2022-05-29 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0019_question_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='file',
        ),
    ]
