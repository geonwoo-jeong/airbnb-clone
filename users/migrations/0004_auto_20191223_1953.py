# Generated by Django 3.0b1 on 2019-12-23 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191117_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(blank=True, choices=[('usd', 'USD'), ('krw', 'KRW'), ('jpy', 'JPY')], default='jpy', max_length=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('kr', 'Korean'), ('jp', 'Japanese')], default='jp', max_length=2),
        ),
    ]