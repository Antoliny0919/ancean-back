# Generated by Django 4.2.11 on 2024-04-04 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_alter_post_is_finish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_finish',
            field=models.BooleanField(default=False),
        ),
    ]
