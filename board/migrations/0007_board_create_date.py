# Generated by Django 4.0.3 on 2022-05-25 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_remove_board_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='create_date',
            field=models.DateTimeField(null=True),
        ),
    ]
