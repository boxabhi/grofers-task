# Generated by Django 3.1.7 on 2021-03-27 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luckydraw', '0002_luckydraws_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize_name', models.CharField(max_length=100)),
                ('prize_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
