# Generated by Django 3.0b1 on 2019-12-30 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_login_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='line_sub',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
