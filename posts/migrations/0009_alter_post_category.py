# Generated by Django 4.2.8 on 2023-12-24 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_color_alter_category_icon'),
        ('posts', '0008_alter_post_author_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, db_column='category', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='category.category'),
        ),
    ]
