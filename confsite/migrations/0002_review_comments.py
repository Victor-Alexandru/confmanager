# Generated by Django 2.2 on 2019-04-18 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comments',
            field=models.CharField(default='', max_length=300, null=True),
        ),
    ]
