# Generated by Django 4.0.3 on 2022-06-05 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0022_remove_question_board2_board_board2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
