# Generated by Django 4.2.11 on 2024-04-04 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_post_header_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_finish',
            field=models.BooleanField(),
        ),
    ]