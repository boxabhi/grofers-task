# Generated by Django 3.1.7 on 2021-03-27 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luckydraw', '0005_auto_20210327_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameparticipants',
            name='is_won',
            field=models.BooleanField(default=False),
        ),
    ]
