# Generated by Django 3.2 on 2021-09-19 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
